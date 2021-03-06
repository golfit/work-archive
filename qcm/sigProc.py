"""

Spectral analysis functions for Numerical python written for
compatability with matlab commands with the same names.

  psd - Power spectral density uing Welch's average periodogram
  csd - Cross spectral density uing Welch's average periodogram
  cohere - Coherence (normalized cross spectral density)
  corrcoef - The matrix of correlation coefficients

The functions are designed to work for real and complex valued Numeric
arrays.

One of the major differences between this code and matlab's is that I
use functions for 'detrend' and 'window', and matlab uses vectors.
This can be easily changed, but I think the functional approach is a
bit more elegant.

Please send comments, questions and bugs to:

Author: John D. Hunter <jdhunter at ace.bsd.uchicago.edu>
MODIFIED: 19 July 2012, Ted Golfinopoulos - changed references to typecode with type() or numpy.iscomplex(), as needed.
"""

from __future__ import division
from MLab import mean, hanning, cov
from Numeric import zeros, ones, diagonal, transpose, matrixmultiply, \
     resize, sqrt, divide, array, Float, Complex, concatenate, \
     convolve, dot, conjugate, absolute, arange, reshape
from FFT import fft
import numpy
#from numpy import numpy.iscomplex, ones
from scipy.signal import hamming

def norm(x):
    return sqrt(dot(x,x))

#def window_hanning(x):
#    return hanning(len(x))*x

def window_hamming(x):
	return hamming(len(x))*x

def window_none(x):
    return x

def detrend_mean(x):
    return x - mean(x)

def detrend_none(x):
    return x

def detrend_linear(x):
    """Remove the best fit line from x"""
    # I'm going to regress x on xx=range(len(x)) and return
    # x - (b*xx+a)
#    xx = arange(len(x), typecode=x.typecode())
    xx=arange(len(x),type(x))
    X = transpose(array([xx]+[x]))
    C = cov(X)
    b = C[0,1]/C[0,0]
    a = mean(x) - b*mean(xx)
    return x-(b*xx+a)


def psd(x, NFFT=256, Fs=2, detrend=detrend_none,
        window=window_hamming, noverlap=0):
    """
    The power spectral density by Welches average periodogram method.
    The vector x is divided into NFFT length segments.  Each segment
    is detrended by function detrend and windowed by function window.
    noperlap gives the length of the overlap between segments.  The
    absolute(fft(segment))**2 of each segment are averaged to compute Pxx,
    with a scaling to correct for power loss due to windowing.  Fs is
    the sampling frequency.

    -- NFFT must be a power of 2
    -- detrend and window are functions, unlike in matlab where they are
       vectors.
    -- if length x < NFFT, it will be zero padded to NFFT
    

    Refs:
      Bendat & Piersol -- Random Data: Analysis and Measurement
        Procedures, John Wiley & Sons (1986)

    """

    if NFFT % 2:
        raise ValueError, 'NFFT must be a power of 2'

    # zero pad x up to NFFT if it is shorter than NFFT
    if len(x)<NFFT:
        n = len(x)
        x = resize(x, (NFFT,))
        x[n:] = 0
    

    # for real x, ignore the negative frequencies
#    if x.typecode()==Complex: numFreqs = NFFT
    if any(numpy.iscomplex(x)) : numFreqs = NFFT
    else: numFreqs = NFFT//2+1
        
#    windowVals = window(ones((NFFT,),x.typecode()))
    windowVals = window(numpy.ones(NFFT))
    step = NFFT-noverlap
    ind = range(0,len(x)-NFFT+1,step)
    n = len(ind)
#    Pxx = zeros((numFreqs,n), Float)
    Pxx=numpy.zeros([numFreqs,n])

    # do the ffts of the slices
    for i in range(n):
        thisX = x[ind[i]:ind[i]+NFFT]
        thisX = windowVals*detrend(thisX)
        fx = absolute(fft(thisX))**2
	#print("numFreqs={0:f}".format(numFreqs))
	#print("len of fx slice={0:d}".format(len(fx[:int(numFreqs)])))
	#print("len of destination in Pxx={0:d}")
        Pxx[:,i] = fx[:int(numFreqs)]

    # Scale the spectrum by the norm of the window to compensate for
    # windowing loss; see Bendat & Piersol Sec 11.5.2
    if n>1: Pxx = mean(Pxx,1)
    Pxx = divide(Pxx, norm(windowVals)**2)
    freqs = Fs/NFFT*arange(0,numFreqs)
    return Pxx, freqs



def csd(x, y, NFFT=256, Fs=2, detrend=detrend_none,
        window=window_hamming, noverlap=0):
    """
    The cross spectral density Pxy by Welches average periodogram
    method.  The vectors x and y are divided into NFFT length
    segments.  Each segment is detrended by function detrend and
    windowed by function window.  noverlap gives the length of the
    overlap between segments.  The product of the direct FFTs of x and
    y are averaged over each segment to compute Pxy, with a scaling to
    correct for power loss due to windowing.  Fs is the sampling
    frequency.

    NFFT must be a power of 2

    Refs:
      Bendat & Piersol -- Random Data: Analysis and Measurement
        Procedures, John Wiley & Sons (1986)

    """

    if NFFT % 2:
        raise ValueError, 'NFFT must be a power of 2'

    # zero pad x and y up to NFFT if they are shorter than NFFT
    if len(x)<NFFT:
        n = len(x)
        x = resize(x, (NFFT,))
        x[n:] = 0
    if len(y)<NFFT:
        n = len(y)
        y = resize(y, (NFFT,))
        y[n:] = 0

    # for real x, ignore the negative frequencies
#    if x.typecode()==Complex: numFreqs = NFFT
    if any(numpy.iscomplex(x)): numFreqs = NFFT
    else: numFreqs = NFFT//2+1
        
#    windowVals = window(ones((NFFT,),x.typecode()))
    windowVals = window(numpy.ones(NFFT))
    step = NFFT-noverlap
    ind = range(0,len(x)-NFFT+1,step)
    n = len(ind)
#    Pxy = zeros((numFreqs,n), Complex)
    Pxy=numpy.zeros([numFreqs,n])

    # do the ffts of the slices
    for i in range(n):
        thisX = x[ind[i]:ind[i]+NFFT]
        thisX = windowVals*detrend(thisX)
        thisY = y[ind[i]:ind[i]+NFFT]
        thisY = windowVals*detrend(thisY)
        fx = fft(thisX)
        fy = fft(thisY)
        Pxy[:,i] = fy[:numFreqs]*conjugate(fx[:numFreqs])

    # Scale the spectrum by the norm of the window to compensate for
    # windowing loss; see Bendat & Piersol Sec 11.5.2
    if n>1: Pxy = mean(Pxy,1)
    Pxy = divide(Pxy, norm(windowVals)**2)
    freqs = Fs/NFFT*arange(0,numFreqs)
    return Pxy, freqs

def cohere(x, y, NFFT=256, Fs=2, detrend=detrend_none,
           window=window_hamming, noverlap=0):
    """
    cohere the coherence between x and y.  Coherence is the normalized
    cross spectral density

    Cxy = |Pxy|^2/(Pxx*Pyy)

    The return value is (Cxy, f), where f are the frequencies of the
    coherence vector.  See the docs for psd and csd for information
    about the function arguments NFFT, detrend, windowm noverlap, as
    well as the methods used to compute Pxy, Pxx and Pyy.

    """

    
    Pxx,f = psd(x, NFFT=NFFT, Fs=Fs, detrend=detrend,
              window=window, noverlap=noverlap)
    Pyy,f = psd(y, NFFT=NFFT, Fs=Fs, detrend=detrend,
              window=window, noverlap=noverlap)
    Pxy,f = csd(x, y, NFFT=NFFT, Fs=Fs, detrend=detrend,
              window=window, noverlap=noverlap)

    Cxy = divide(absolute(Pxy)**2, Pxx*Pyy)
    return Cxy, f

def corrcoef(*args):
    """
    
    corrcoef(X) where X is a matrix returns a matrix of correlation
    coefficients for each row of X.
    
    corrcoef(x,y) where x and y are vectors returns the matrix or
    correlation coefficients for x and y.

    Numeric arrays can be real or complex

    The correlation matrix is defined from the covariance matrix C as

    r(i,j) = C[i,j] / (C[i,i]*C[j,j])
    """

    if len(args)==2:
        X = transpose(array([args[0]]+[args[1]]))
    elif len(args==1):
        X = args[0]
    else:
        raise RuntimeError, 'Only expecting 1 or 2 arguments'

    
    C = cov(X)
    d = resize(diagonal(C), (2,1))
    r = divide(C,sqrt(matrixmultiply(d,transpose(d))))[0,1]
    try: return r.real
    except AttributeError: return r

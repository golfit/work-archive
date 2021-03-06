from numpy import *
import pdb
from myTools_no_sql import myDownsampleWithSmooth, bp, lp

def calcTransFun(y,xHilb,fRange,fs,fMin=None) :
    """
    #This function calculates the transfer function of two signals, H=y/x, given the signal, y, and x+1j*hilbert(x).  It is agnostic of the MDsplus tree.

    The transfer function is calculated according to

    H ~= LP{ bp(y(t)) * bp(conj(x(t)+1j*hilbert(x(t)))) } / LP( bp(x(t))^2 )

    #USAGE: H=calcTransFun(y,xHilb,fRange,fs[,fMin])
        INPUT:
            y=output (numerator) signal in time domain.  Real-valued numpy array.
            xHilb = x(t) + 1j*hilbert(x(t)).  Real part is original input (denominator) signal in time domain.  Imaginary part is Hilbert transform of x
            fRange = array with two elements, [flow, fhigh], specifying lower and upper frequencies (in Hz) of frequency band in which to calculate transfer function
            fs=sampling frequency of y and x (must be the same for both signals)
            fMin = optional argument.  Upper frequency at which transfer function is band-limited.  Should be much less than min(fRange).  Default=0.01*min(fRange)

        OUTPUT:
            H=transfer function over specified frequency range.  In time-domain, down-sampled according to fMin (i.e. sampling frequency of H = 2*fMin)
    #
    #Ted Golfinopoulos, 7 June 2012
    #See also Matlab function, syncDetect (my function)
    """
    print('Calculating transfer function')
    if(len(fRange) != 2) :
        raise IOError('fRange must be two-element array containing lower and upper frequencies')

    fLow=min(fRange)
    fHigh=max(fRange)

    #If no value for fMin is defined, calculate default value
    if fMin is None :
        fMin=0.01*fLow
    elif (fMin>fLow) :
        raise IOError('fMin must be > lower frequency of band in which transfer function is calculated')
    print('Preparing to calculate bandpass-filtered signals')
    ybp = bp(y,fs,fLow,fHigh)
    print('Calculated ybp')
    #Band-pass filter y and real and imaginary parts of x.
    xrbp = bp(real(xHilb),fs,fLow,fHigh)
    print('Calculated xrbp')
    xibp = bp(imag(xHilb),fs,fLow,fHigh)
    print('Calculated xibp')
    print('Applied bandpass filters')
    
    #Calculate real and imaginary parts of transfer function
    #Double fMin so that fMin is the Nyquist frequency of the transfer function
    #Note that * and / are element-wise binary operators in Python
    Hr = lp( ybp * xrbp, fs, 2.*fMin ) / lp( pow(xrbp,2), fs, 2.*fMin )
    Hi = -lp( ybp * xibp, fs, 2.*fMin ) / lp( pow(xrbp,2), fs, 2.*fMin ) #negative sign to effect complex conjugate of x
    print('Calculated real and imaginary parts of transfer function')

    #pdb.set_trace()

    #Now, down-sample transfer function, since it is band-limited by fMin.
    #Smooth first using a moving average.
    #Return complex transfer function
    downsampleRatio = int(floor( fs/(2.*fMin) ))

    #return myDownsample(Hr,downsampleRatio)+1j*myDownsample(Hi,downsampleRatio)
    #return myDownsample(smooth(Hr,downsampleRatio),downsampleRatio)+1j*myDownsample(smooth(Hi,downsampleRatio),downsampleRatio)
    return myDownsampleWithSmooth(Hr,downsampleRatio) + 1j*myDownsampleWithSmooth(Hi,downsampleRatio)

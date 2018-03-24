#Module containing useful functions.  Note that the numpy library is used!!!
#2 Feb 2012, Ted Golfinopoulos

from MDSplus import *
import numpy
import numpy as np
import scipy
import scipy.fftpack
import re
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
#import matplotlib.pyplot as plt
import pdb
from scipy.interpolate import interp1d
from scipy.signal import convolve2d
import sys

import MDSplus as mds

def dec2bin(decimal_number,min_digits=None) :
    '''
    Clone of Matlab dec2bin function.

    USAGE:
    dec2bin(decimal_number,min_digits=None)

    returns a string representation of decimal_number.

    If min_digits is specified, then the binary number will contain at least min_digits, zero-filling up to min_digits of the length of the binary number is less than min_digits.

    Ted Golfinopoulos, 16 May 2015
    '''
    if(min_digits==None) :
        return "{0:b}".format(decimal_number)
    else :
        return ("{0:"+str(min_digits)+"b}").format(decimal_number).replace("\s","0")

def find(x) :
	"""
	Return indices of all elements with a true logic value.
	This is implemented in the pylab library, but we don't have
	access to this on alcdaq3, so here is a "temporary" kluge.

	Dependency on numpy!!!
	"""
	output=[] #Initialize (integer) vector of indices.
	for i in range(0,len(x)) :
		if(x[i]) : output.append(int(i)) #If x[i] is true, store index.
	return numpy.core.multiarray.array(output) #Wrap in an array object so that operator arithmetic integers is possible.

def smooth(x, numPoints) :
	"""
	Use numpy convolve function to implement a moving-window average of the data.

	Ted Golfinopoulos, 16 July 2012
	"""
	window=numpy.ones(numPoints)/numPoints #Window for moving average filter
	return numpy.convolve(x,window,'same')


def bp(x, fs, fLow, fHigh) :
	"""
	Band-pass filter implemented as top-hat function in frequency domain (via discrete Fourier transform)

	USAGE:
		y=bp(x, fs, fLow, fHigh)
	INPUT:
		x=input signal
		fs=sampling frequency [Hz]
		fLow=lower frequency in pass band [Hz]
		fHigh=upper frequency in pass band [Hz]
	OUTPUT: y=band-pass-filtered signal

	Ted Golfinopoulos, 7 June 2012
	"""

	#Input check
	if(fLow > fHigh) :
		raise IOError('fLow must be < fHigh')

	if(fHigh > fs ) :
		raise IOError('fs must be > fHigh')

	#Calculate one-sided Fourier transform of signal.
	[X,f]=myRfft(x,fs) #Compute real fast Fourier transform
	X[numpy.logical_and(f<fLow,f>fHigh)]=0. #Zero out parts of Fourier transform outside of pass band.

	#Band-limit X, transform back to Fourier domain, and return to caller
	return scipy.fftpack.irfft( X ) #Note: numpy.logical_and() is like Matlab &

def hp(x, fs, fLow) :
	"""
	High-pass filter implemented as step function in frequency domain (via discrete Fourier transform)

	USAGE:
		y=hp(x, fs, fLow)
	INPUT:
		x=input signal
		fs=sampling frequency [Hz]
		fLow=lower frequency in pass band [Hz] - pass above this frequency
	OUTPUT: y=band-pass-filtered signal

	Ted Golfinopoulos, 7 June 2012
	"""

	#Input check
	if(fLow > 0.5*fs ) :
		raise IOError('0.5*fs must be > fLow')

	#Calculate one-sided Fourier transform of signal.
	[X,f]=myRfft(x,fs) #Compute real fast Fourier transform
	X[f<fLow]=0. #Zero out parts of Fourier transform outside of pass band.

	#Pass components of X above fLow, transform back to Fourier domain, and return to caller
	return scipy.fftpack.irfft( X )

def lp(x, fs, fHigh) :
	"""
	Low-pass filter implemented as step function in frequency domain (via discrete Fourier transform)

	USAGE:
		y=lp(x, fs, fHigh)
	INPUT:
		x=input signal
		fs=sampling frequency [Hz]
		fHigh=upper frequency in pass band [Hz] - pass beneath this frequency
	OUTPUT: y=band-pass-filtered signal

	Ted Golfinopoulos, 7 June 2012
	"""

	#Input check
	if(fHigh > fs*0.5 ) :
		raise IOError('fs*0.5 must be > fHigh')

	#Calculate one-sided Fourier transform of signal.
	[X,f]=myRfft(x,fs) #Compute real fast Fourier transform
	X[f>fHigh]=0. #Zero out parts of Fourier transform outside of pass band.

	#Band-limit X, transform back to Fourier domain, and return to caller
	return scipy.fftpack.irfft( X )
	

def myRfft(y, fs) :
	"""
	Right-handed fast Fourier transform using scipy.fftpack.rfft
	USAGE:
		Y,f=myRfft(y,fs)
		y=signal to transform (time domain)
		fs=sampling frequency
		Y=transformed signal (Fourier domain, positive frequencies, only)
		f=frequency axis of Y (same units as fs), f>=0
	Ted Golfinopoulos, 7 June 2012
	"""
	Y=scipy.fftpack.rfft(y)
	f=(fs/2.E0)*numpy.linspace(0.E0,1.E0,len(Y))
	return [Y,f]

def myDownsample(y, N) :
	"""
	yds = myDownsample(y,N)

	yds is y sampled at every Nth index, starting with yds[0]=y[0] with y[range(0,len(y),N)].  Implementing Matlab's downsample.
	Ted Golfinopoulos, 7 June 2012
	"""

	return y[range(0,len(y),N)]


def myDownsampleWithSmooth(y, N) :
	"""
	yds = myDownsampleWithSmooth(y,N)

	yds is y sampled at every Nth index, starting with yds[0]=y[0] with y[range(0,len(y),N)], but y is first averaged across all N points centered on the selected index.  Boundary conditions: no wrap around.
	Ted Golfinopoulos, 16 June 2012
	"""

	jj=0;
	ynew=numpy.zeros( 1 + int((len(y)-1)/N) )
	for ii in range(0,len(y),N) :
		lowerBound=min(max(0,ii-numpy.ceil(N*0.5)), len(y)-1-numpy.ceil(N*0.5))
		upperBound=min(lowerBound+numpy.floor(N*0.5),len(y)-1)
		ynew[jj]=numpy.mean( y[ lowerBound:upperBound ] )
		jj=jj+1

	return ynew

def searchSubnodes( nodeList, regExpr ) :
	"""
	This function searches the names of nodeList for matches with a regular expression, and returns the sublist which matches.

	Example:
	matchedNodes = searchSubnodes( nodeList, regExpr )

	Ted Golfinopoulos, 24 June 2015
	"""

	matchedNodes=list() #Initialize empty list of nodes that match

	for index in range(0,len(nodeList)) :
		if( re.match( str.lower(regExpr),  str(nodeList[index].getFullPath()).lower() ) and len(str(nodeList[index].getFullPath()))!=0 ) :
			matchedNodes.append(index)

	if(len(matchedNodes)!=0) :
		return [nodeList[ii] for ii in matchedNodes]
	else :
		return [] #Return empty list
	
def parseList(myStr) :
	"""
	This function parses a list of integers from a string.  Commas separate individual entries; a colon indicates a range (inclusive)range
	Ex.: myStr='1,3:5,11'
	myList=parseList(myStr)

	myList contains [1,3,4,5,11]

	This function depends on regular expression library.
	Ted Golfinopoulos, 7 June 2012
	"""

	elems=re.split(',|\+|\[|\]',myStr) #Split at commas for list, or + if some offset is added.

	cmdStr="" #Command string - intialize.	
	for substr in elems :
		if(len(cmdStr)==0) :
			 #Open concatenation to put shot list in single array.
			#Kluge: give an empty array as first argument in case
			#there is only one shot arg in list, since concatenate can't handle cast where there is only one input
			cmdStr="numpy.core.multiarray.concatenate(([],"
		else :
			cmdStr=cmdStr+',' #Add comma for concatenation
		if( re.match("(\d+:\d+){1,1}", substr) ) :
			start,end=re.split(':',substr)
			substr='range('+start+','+end+'+1)' #Replace substring by Python range function.  +1 is to make range inclusive.
		else :
			substr="["+substr+"]" #Bracket every integer for concatenation into a single array.

		cmdStr=cmdStr+substr

	cmdStr=cmdStr+"))" #Close concatenating operation

	try :
		myList=eval(cmdStr)
		#Add additional step of converting arguments to integers.
		return [int(s) for s in myList]
	except :
		print("Command string ... "+cmdStr+" ... couldn't be executed.")

def parsePremadeNodeList(stringArgs, s) :
	nodeList=[]
	ceceNodes=[]

	#Define which nodes to get signals for
	if(any([x=="allmag" for x in stringArgs]) or any([x=="all_mag" for x in stringArgs])) :
		print('All active magnetics coils will be processed.')
		#Fetch all active signals from ACTIVE_MHD.SIGNALS
		magTree=Tree('magnetics',s)
		nList=magTree.getNode('active_mhd.signals').getNodeWild('*')
		onState=nList.isOn()
		isSignal=[x=='SIGNAL' for x in nList.getUsage()]
		nodeList=nList.getFullPath()
		nodeList=nodeList[find(numpy.logical_and( isSignal, onState ))]
		nodeList=[x.strip() for x in nodeList] #Take white space off of node list.
		
	elif(any([x=="somemag" for x in stringArgs]) or any([x=="some_mag" for x in stringArgs])) :
		print('A subset of magnetics coils will be processed.')
		#Process the transfer functions of a subset of Mirnov coil proves.
		nodeList=['bp_ab_top', 'bp_bc_bot', 'bp_bc_top', 'bp_ef_bot', 'bp1t_abk', 'bp1t_ghk', 'bp3t_ghk', 'bp2t_abk', 'bp5t_ghk', 'bp5t_abk', 'bp_ef_top', 'bp_ka_bot', 'bp_ka_top']
		nodePath='\\magnetics::top.active_mhd.signals.' #Pre-pend path to signals
		nodeList=[nodePath+x for x in nodeList]

	if(any([x=="asp" for x in stringArgs])) :
		#regexpr='(bdot\d{1,2}\>)|(density_fit)|(phi_fit)|(te_fit)'; %Only get the polarimeter nodes like frot_01, frot_02, and frot_03; don't allow suffixes on these names.

		print('The ASP nodes will be processed.')
		edgeTree=Tree('edge',s)
		#Grab all ASP nodes associated with MLP (only fit quantities) or Mirnov coil mounts.
		aspNodeObj=searchSubnodes(edgeTree.getNodeWild('probes.asp.***'),'.*mlp.p\d.*fit')

		#aspNodes=['DN:BDOT1','UP:BDOT1','DN:BDOT5','UP:BDOT5', 'DN:BDOT25','UP:BDOT25','DN:BDOT50','UP:BDOT50','']
		#nodePath='\\EDGE::TOP.PROBES.ASP.MAG.'
		#aspNodes=[nodePath+x for x in aspNodes]
		aspNodes=[str(n.getFullPath()) for n in aspNodeObj]
		nodeList=nodeList + aspNodes #Concatenate asp nodes onto node list.

	if(any([x=="aspmag" for x in stringArgs])) :
		#regexpr='(bdot\d{1,2}\>)|(density_fit)|(phi_fit)|(te_fit)'; %Only get the polarimeter nodes like frot_01, frot_02, and frot_03; don't allow suffixes on these names.

		print('The ASP magnetic nodes will be processed.')
		edgeTree=Tree('edge',s)
		#Grab all ASP nodes associated with MLP (only fit quantities) or Mirnov coil mounts.
		aspNodeObj=searchSubnodes(edgeTree.getNodeWild('probes.asp.***'),'.*mag.up.bdot.*|.*mag.dn.bdot.*')
		aspNodes=[str(n.getFullPath()) for n in aspNodeObj]
		nodeList=nodeList + aspNodes #Concatenate asp nodes onto node list.

	if(any([x=="pci" for x in stringArgs])) :
		print('All PCI chords will be processed.')
		nodePath='\\pcilocal::top.results.'
		pciNodes=[nodePath+"pci_{0:>02}".format(x) for x in range(1,32+1)]
		nodeList=nodeList + pciNodes #Concatenate pci nodes onto node list.

	if(any([x=="polarimeter" for x in stringArgs]) or any([x=="polar" for x in stringArgs])) :
		print("Polarimeter chords 1-3 will be processed.")
		nodePath='\ELECTRONS::TOP.POLARIMETER.RESULTS:'
		polarimeterNodes=[nodePath+"frot_0{0:d}".format(x) for x in range(1,3+1)]
		nodeList=nodeList + polarimeterNodes #Concatenate polarimeter nodes onto node list.

	if(any([x=="cece" for x in stringArgs])) :
		print('The CECE nodes will be processed.')
		nodePath='\ELECTRONS::TOP.CECE.HARDWARE:ACQ216:'
		ceceNodesI=[nodePath+"input_{0:>02}".format(x) for x in [5, 10, 12, 15]]
		ceceNodesQ=[nodePath+"input_{0:>02}".format(x) for x in [6, 11, 14, 16]]
		ceceNodes=[[ceceNodesI[i],ceceNodesQ[i]] for i in range(0,len(ceceNodesI)) ]
		nodeList=ceceNodesI

	return nodeList,ceceNodes

def getYX(n) :
	"""
	Usage: y,t=getYX(n)

		INPUT:
			MDS node object, n

		OUTPUT: tuple y,t containing the signal and its timebase.  Syntactic sugar for
			y=n.getData().evaluate.data()
			t=n.getData().evaluate().dim_of().data()
	"""
	return (n.getData().evaluate().data(), n.getData().evaluate().dim_of().data())

def getDataInRange(n,t1,t2) :
	"""
	Grab data from an MDS signal node in a specified subset of the timebase.
	USAGE:
		y,t=getDataInRange(srcNode,t1,t2)

		srcNode is an MDSplus node object
		t1 and t2 are the start and stop times of the timebase subset in which to grab data
		y is the signal in the specified range
		t is the corresponding timebase, generated internally in Python from start and stop times extracted from the database.
	"""
	myStr="_y="+n.getPath()+", _t=dim_of("+n.getPath()+"), pack(_y, _t > {0:f} and _t < {0:f})".format(t1,t2)
	t1Actual=mds.mdsdata.Data.compile("_t=dim_of("+n.getPath()+ "), _t[firstloc(_t > {0:f} and _t < {0:f})]".format(t1,t2) ).evaluate().data()
	t2Actual=mds.mdsdata.Data.compile("_t=dim_of("+n.getPath()+ "), _t[lastloc(_t > {0:f} and _t < {0:f})]".format(t1,t2) ).evaluate().data()
	y=mds.mdsdata.Data.compile( myStr ).evaluate().data() #Grab data in specified range
	return y, numpy.linspace(t1Actual,t2Actual,len(y)) #Regenerate timebase locally

#def cohereSpecgram(x, y, NFFT=256, Fs=2, nxavg=6, nyavg=6, detrend=mlab.detrend_none, window=mlab.window_hanning, noverlap=0, pad_to=None, sides='default', scale_by_freq=None) :
#	"""
#	Use matplotlib mlab functions to synthesize a cross-coherence (normalized cross spectral density,
#	|Pxy^2|/(Pxx*Pxy)) spectrogram.  The periodogram methods for calculating cross- and autocorrelation
#	functions calculate binned short-time Fourier transforms and average across them.
#	The binned spectra can be analyzed before averaging.  mlab uses _spectral_helper to compute the
#	power- and cross-spectral densities (used to calculate cross-coherence), as well as the specgram.
#	Here, we calculate the cross-coherence function returning the values at individual short-time bins.
#
#	USAGE:
#		Cxy, freqs, t = cohereSpecgram(x, y, nxavg=6, nyavg=6, NFFT=256, Fs=2, detrend=mlab.detrend_none, window=window_hanning, noverlap=0, pad_to=None, sides='default', scale_by_freq=None) :
#
#		nxavg=number of time bins to average over when computing cross-coherence.  Default=6.
#		nyavg=number of frequency bins to average over when computing cross-coherence.  Default=6.
#
#	Cxy = cross-coherence function, Pxy^2/(Pxx*Pxy), resolved at frequency and time points.  Differs from cohere not only from time resolution, but also in that it is complex
#	(do not take absolute value of Pxy).  The phase information is available in this way.
#	freqs = frequency axis of Cxy.
#	t = time axis of Cxy
#
#	Ted Golfinopoulos, 15 Aug 2012
#	"""
#	assert(len(x)==len(y))
#
#	Pxy, freqs, t = mlab._spectral_helper(x, y, NFFT, Fs, detrend, window, noverlap, pad_to, sides, scale_by_freq)
#	Pxx = mlab._spectral_helper(x, x, NFFT, Fs, detrend, window, noverlap, pad_to, sides, scale_by_freq)
#	Pyy = mlab._spectral_helper(y, y, NFFT, Fs, detrend, window, noverlap, pad_to, sides, scale_by_freq)
#
#	Pxx=Pxx[0].real
#	Pyy=Pyy[0].real
#
#	w=numpy.empty([nyavg,nxavg])
#	w[:]=1./(nxavg*nyavg)
#
#	Cxy=convolve2d(Pxy,w,'same','symm')**2/(convolve2d(Pxx,w,'same','symm')*convolve2d(Pyy,w,'same','symm'))
#
#	return Cxy, freqs, t

def window_hamming(x):
	"""
		This function is analogous to window_hanning of matplotlib.mlab.  It returns the hamming window of the same length as the input, multiplied by the input.
		USAGE:
			windowedX=window_hamming(x)

		The Hamming window is defined as w(n) = 0.54+0.46*cos(2*pi*n/(M-1)), 0<=n<=M-1

	Ted Golfinopoulos, 1 March 2013
	"""
	return np.hamming(len(x))*x

def cohereSpecgram(x, y, NFFT=256, Fs=2, nxavg=8, detrend=mlab.detrend_none, window=window_hamming, noverlap=0, pad_to=None, sides='default', scale_by_freq=None):
    """
	This function is based on _spectral_helper from matplotlib.mlab, which implements the commonality between the
	psd, csd, and spectrogram.  I adapt it here to provide the cross spectral density on the windowed segments.

	The function works as follows: x and y are broken up into windowed segments of length, NFFT*nxavg.  The cross power spectral density of these windowed segments are then calculated using the matplotlib.mlab.csd function.  This function computes the CSD by breaking the signal into windowed segments of length, NFFT, computing the CSD of each 

	USAGE:
			Cxy, freqs, t = cohereSpecgram(x, y, nxavg=8, NFFT=256, Fs=2, detrend=mlab.detrend_none, window=window_hamming, noverlap=0, pad_to=None, sides='default', scale_by_freq=None) :

		window_hamming is defined in myTools and is the function specifying the hamming window multiplied by the input
		noverlap is associated with the overlap used in the signal processing within each "spectrogram" bin.  The overlap between these bins has the same ratio to bin size as noverlap has to nfft - in other words, it is noverlap*nxavg.

		Cxy = cross-coherence function, Pxy/sqrt(Pxx*Pxy), resolved at frequency and time points.  Differs from cohere not only from time resolution, but also in that it is complex, and it is not the magnitude squared value.  This is so that the phase angle does not get doubled and then make unwrapping difficult.
		freqs = frequency axis of Cxy.
		t = time axis of Cxy

		Ted Golfinopoulos, 1 Mar 2013
    """
    #This checks for if y is x are so that we can use the same function to
    #implement the core of psd(), csd(), and spectrogram() without doing
    #extra calculations. We return the unaveraged Pxy, freqs, and t.
    same_data = numpy.all(y==x) #This used the "is" function, y is x, originally, but that failed.

    specNfft = NFFT*nxavg #This is the number of points in the bins at the spectrogram level - the larger level window

    specNoverlap=noverlap*nxavg

    #Make sure we're dealing with a numpy array. If y and x were the same
    #object to start with, keep them that way
    x = np.asarray(x)
    if ( not same_data ):
        y = np.asarray(y)
    else:
        y = x

    # zero pad x and y up to specNfft if they are shorter than specNfft
    if len(x)<specNfft:
        n = len(x)
        x = np.resize(x, (specNfft,))
        x[n:] = 0

    if not same_data and len(y)<specNfft:
        n = len(y)
        y = np.resize(y, (specNfft,))
        y[n:] = 0

    if pad_to is None:
        pad_to = NFFT #This corresponds to padding inside the psd and csd functions, which take bins of data of sice, specNfft.  Use the smaller value of pad_to

    if scale_by_freq is None:
        scale_by_freq = True

    # For real x, ignore the negative frequencies unless told otherwise
    if (sides == 'default' and np.iscomplexobj(x)) or sides == 'twosided':
        numFreqs = pad_to
        scaling_factor = 1.
    elif sides in ('default', 'onesided'):
        numFreqs = pad_to//2 + 1
        scaling_factor = 2.
    else:
        raise ValueError("sides must be one of: 'default', 'onesided', or "
            "'twosided'")

    if cbook.iterable(window):
        assert(len(window) == specNfft)
        windowVals = window
    else:
        windowVals = window(np.ones((specNfft,), x.dtype))

    step = specNfft - specNoverlap
    ind = np.arange(0, len(x) - specNfft + 1, step)
    n = len(ind)
    #Pxy = np.zeros((numFreqs, n), np.complex_)
    Cxy = np.zeros((numFreqs, n), np.complex_)

    # do the ffts of the slices
    for i in range(n):
        thisX = x[ind[i]:ind[i]+specNfft]
        thisX = windowVals * detrend(thisX)
	Pxx,ff=mlab.psd(thisX, NFFT, Fs, detrend, window, noverlap, pad_to, sides, scale_by_freq)
#        fx = np.fft.fft(thisX, n=pad_to)

        if same_data:
            Pyy = Pxx
	    Pxy = Pxx
        else:
            thisY = y[ind[i]:ind[i]+specNfft]
            thisY = windowVals * detrend(thisY)
#            fy = np.fft.fft(thisY, n=pad_to)
	    Pyy,ff=mlab.psd(thisY, NFFT, Fs, detrend, window, noverlap, pad_to, sides, scale_by_freq)
	    Pxy,ff=mlab.csd(thisX, thisY, NFFT, Fs, detrend, window, noverlap, pad_to, sides, scale_by_freq)
        Cxy[:,i] = Pxy/np.sqrt(Pxx*Pyy)

    t = 1./Fs * (ind + specNfft / 2.)
    #freqs = float(Fs) / pad_to * np.arange(numFreqs)
    freqs=ff #Frequency output from psd and csd.

    if (np.iscomplexobj(x) and sides == 'default') or sides == 'twosided':
        # center the frequency range at zero
        freqs = np.concatenate((freqs[numFreqs//2:] - Fs, freqs[:numFreqs//2]))
        Cxy = np.concatenate((Cxy[numFreqs//2:, :], Cxy[:numFreqs//2, :]), 0)

    return Cxy, freqs, t

def crossSpecgram(x, y, NFFT=256, Fs=2, detrend=mlab.detrend_none, window=mlab.window_hanning, noverlap=0, pad_to=None, sides='default', scale_by_freq=None) :
	"""
	Use matplotlib.mlab function, _spectral_helper, to calculate cross power between x and y in short time bins.

	USAGE:
		Pxy,freqs,t=crossSpecgram(x,y,NFFT=256, Fs=2, detrend=mlab.detrend_none, window=window_hanning, noverlap=0, pad_to=None, sides='default', scale_by_freq=None)

	NFFT=# data points in each time bin
	Fs = sample frequency in units of 1/[x]
	etc. - as in other mlab functions.

	Pxy=cross power
	Ted Golfinopoulos, 15 Aug 2012
	"""
	assert(len(x)==len(y))

	Pxy, freqs, t = mlab._spectral_helper(x, y, NFFT, Fs, detrend, window, noverlap, pad_to, sides, scale_by_freq)

	return Pxy, freqs, t
	


#for substr in elems :
#		if(len(cmdStr)==0) :
#			 #Open concatenation to put shot list in single array.
#			#Kluge: give an empty array as first argument in case
#			#there is only one shot arg in list, since concatenate can't handle cast where there is only one input
#			cmdStr="numpy.core.multiarray.concatenate(([],"
#		else :
#			cmdStr=cmdStr+',' #Add comma for concatenation
#		if( re.match("(\d+:\d+){1,1}", substr) ) :
#			start,end=re.split(':',substr)
#			substr='range('+start+','+end+'+1)' #Replace substring by Python range function.  +1 is to make range inclusive.
#		else :
#			substr="["+substr+"]" #Bracket every integer for concatenation into a single array.

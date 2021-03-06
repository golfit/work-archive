#Import libraries.
#import pdb
from numpy import *
# from scipy import *
# from matplotlib import *
#from pylab import * #Has "find" function, I think
from myTools import * #Since pylab isn't available on alcdaq3, homemade "find" was added to myTools module.

def decodeSignal(y, t, fclk, nbits) :
	"""
	This file reads in digitized voltages outputted from the
	QCM Antenna Master Controller Board and outputs time,logic code number
	pairs.

	The encoding scheme is as follows:
	HEADER: 3 clock cycles HIGH, followed by 3 clock cycles LOW
	SIGNAL: 1 clock cycle LOW, followed by 1 clock cycle HIGH or LOW depending on logic state of bit, followed by 
		another clock cycle LOW
	CLOSER: 1 clock cycle LOW, followed by 2 clock cycles HIGH.

	Ex. USAGE:
		...
		fclk=4.E6
		nbits=7
		t,y = decodeSig(y,t, fclk, nbits)

	y = array of double-precision numbers giving voltage signal with encoded numbers
	t = array of double-precision numbers giving timebase of signal
	fclk = Clock speed of output, which is master controller board's clock speed divided by 16, since least significant bit of counter is only toggled on clock positive edges [Hz]
	nbits = number of bits encoded in signal.

	Begun on Tuesday, 17 January 2012 (my 28th Birthday!), Ted Golfinopoulos
	"""

	tauc=1./fclk #Period of master controller board clock, [s]
	taus=t[1]-t[0] #Sampling time
	fs=1.E0/taus #Sampling frequency.

	onThresh=1.0E0 #Threshold voltage above which the signal is considered ON.

	#Duration of an encoded logic transmission, including header (6 clock cycles),
	#bit encoding, and closer (3 clock cycles) [s]
	dt = (9.E0+nbits*3.E0)*tauc 
	tbin = 3.E0*tauc

	#Find indice and times times where board output is high
	onSamplesInHeader=int(3.E0*tauc/taus) #Number of digitizer samples expected to be high in header.
	onSamplesInCloser=int(2.E0*tauc/taus) #Number of digitizer samples expected to be low in closer.
	codeLength=int(dt/taus) #Number of samples expected in whole code.

	###Nomenclature:
	#header = characteristic pattern at the start of an encoded signal.
	#	Here, it is 3 clock counts HIGH, followed by 3 clock counts LOW
	#closer = characteristic pattern at the end of an encoded signal.
	#	Here, it is 1 clock count LOW, followed by 2 clock counts HIGH


	#Find indices at which headers and closers start.
	#The algorithm that follows looks for stretches of points where the signal is HIGH for a given
	#duration - the header is high for 3 counts, the closer for 2, and encoded signal bits for 1.
	#There may be some spread in the actual number of points registering as HIGH; as such, the algorithm
	#returns the index of the first point for which the subsequent sequence of points is HIGH for the expected
	#time period, then advances the index pointer by (a) if header, the nominal number of time points in the
	#encoded stream, less the closer, or (b) if closer, the nominal number of time points in the closer.
	#This avoids double-counting.
	#The resulting indices delimit the boundaries of encoded numbers.
	headInds=[]
	closeInds=[]
	bufferLength=0;
	
	i=0 # Initialize index pointer
	while i < len(y) :
		if(y[i]>onThresh) : #First, check if y[i] is on - save computation of comparing series.
			if(all(y[(i+bufferLength):(i+onSamplesInHeader-bufferLength)]>onThresh)) : #Header found - store and jump to end of header ON code.
				headInds.append(i)
				i=i+codeLength-onSamplesInCloser
				continue
			#Don't start marking closers until a header has been found - this can be important if MCB starts putting outputs before the outputs signal digitization starts.
			elif(all(y[(i+bufferLength):(i+onSamplesInCloser-bufferLength)]>onThresh) and len(headInds)>0) :
				closeInds.append(i) #Start index of closer found - store.  Code is between these two indices.
				i=i+onSamplesInCloser
				continue
		i=i+1 #Increment index

	print("Finished finding headers and closers.")
	
	# Takes an array containing a list of bits which are on in a binary number, in any order, with least-significant value corresponding to 0, and returns the decimal number corresponding to this number.
	def onBits2num(bitInds) :
		if len(bitInds)==0 : return 0
		else : return sum([ pow(2,aa) for aa in bitInds ])

	#Preallocate arrays.
	codeVals=zeros(len(closeInds)) #Array to store encoded numbers
	timeVals=zeros(len(closeInds)) #Array to store timepoints at which encoded numbers were sampled

	#Loop through all indices containing the start and end times for encoded bit patterns
	for i in range( 0, len(closeInds) ) :
		#Within each encoded segment, divide up the segment into bins of duration, tbin.
		#The state of the bits are contained in each bin.  Find and number the bins for which the
		#board output was high.
		try :
			tOnInBin= t[headInds[i]+find( y[headInds[i]:closeInds[i]]>onThresh )] - t[headInds[i]]
			codeInds=find([tOnInBin[jj]>2.E0*tbin and tOnInBin[jj]<(2.E0+nbits)*tbin for jj in range(0,len(tOnInBin))])
		except :
			temp=headInds[i:i+5]
			print(i)
			print('headInds')
			print(len(headInds))
			print(temp)
			temp=closeInds[i:i+5]
			print('closeInds')
			print(len(closeInds))
			print(temp)
			temp=find( y[headInds[i]:closeInds[i]]>onThresh )
			print('length of find( y[headInds[i]:closeInds[i]]>onThresh )')
			print(len(temp))
			print('First value')
			print(temp[0])
			raise #Re-raise the exception.

		 #Don't try to index into tOnInBin with array unless array is not empty.  If array is empty, the logic code is 0, and the signal is low for the entire code segment.
		if(len(codeInds)>0) :
			tOnInBin= tOnInBin[ codeInds ]
			tOnInBin=tOnInBin-2.E0*tbin #Subtract time equivalent to first two time bins from signal - these are for the header.
		else : tOnInBin = []

		onBins = unique([ int(aa) for aa in tOnInBin/tbin ])
		#The first two bins (i.e t>0 and t < 2*tbin) comprise the header.
		#Remove these bins from consideration.  The remaining internal bins comprise the logic signal,
		#ordered most-to-least significant bit.  Turn these numbers into the 2's place to simplify conversion
		#into a decimal number.
		onBits = (nbits - 1) - onBins
		#Convert array showing which places are 1 in the binary number into a decimal number.  Store.
		codeVals[i] = onBits2num(onBits)
		timeVals[i] = t[headInds[i]]-0.5*taus #Store timepoint.  On average, time point is halfway between data points around the edge.

	print("Finished calculating codes.")

	#Return vectors of time points and corresponding code values.
	return [timeVals, codeVals]

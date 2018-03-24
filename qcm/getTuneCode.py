# This file reads in digitized voltages outputted from the
# QCM Antenna Master Controller Board and outputs time,logic code number
# pairs.
#
# Tuesday, 17 January 2012 (my 28th Birthday!), Ted Golfinopoulos

from numpy import *
from scipy import *
from matplotlib import *
from pylab import * #Has "find" function, I think

#fpath="/media/USB DISK/qcm/MasterControllerBoardTests/C1SerialChannelLogicOutputTestFallingFreqNcount.dat"
#fpath="/media/USB DISK/qcm/MasterControllerBoardTests/C1SerialChannelLogicOutputTestRisingFreqNcount.dat"
#fpath="/media/USB DISK/qcm/MasterControllerBoardTests/C1SerialChannelLogicOutputTestN225to295kHzIn2s.dat"
#fpath="/media/USB DISK/qcm/MasterControllerBoardTests/C1SerialChannelLogicOutputTestN225to295kHzIn1s.dat"
#fpath="/media/USB DISK/qcm/MasterControllerBoardTests/C1SerialChannelLogicOutputTestN225to295kHzIn0pt1s.dat"
#fpath="/media/USB DISK/qcm/MasterControllerBoardTests/C3SerialNclkTestN225to295kHzIn0pt5s.dat"
fpath="/media/USB DISK/qcm/MasterControllerBoardTests/C1SerialLogicTestN225to295kHzIn0pt5sGoesWithNclkTest.dat"
#Load data
dat=numpy.loadtxt(fpath)

#t=dat[:,0][dat[:,0]<2.20296];
#y=dat[:,1][dat[:,0]<2.20296];
t=dat[:,0]
y=dat[:,1]

#C3SerialNclkTestN225to295kHzIn0pt5s.dat has a closer at the beginning of the sample - cut.
#Also, maybe missing the closer at end - cut
#t=dat[10:,0]
#y=dat[10:,1]

fclk=4.E6/16.E0 #Clock speed of output, which is master controller board's clock speed divided by 16, since least significant bit of counter is only toggled on clock positive edges [Hz]
tauc=1./fclk #Period of master controller board clock, [s]
nbits=7 #Number of bits in MCB logic signal
#nbits=14 #Number of bits in MCB n_clk signal
taus=t[1]-t[0] #Sampling time
fs=1.E0/taus #Sampling frequency.


dt = (9.E0+nbits*3.E0)*tauc #Duration of an encoded logic transmission, including header (6 clock cycles), bit encoding, and closer (3 clock cycles) [s]
tbin = 3.E0*tauc

#Find indice and times times where board output is high
onInds=find(y>1.E0) #output is "ON" at these indices.
onTimes = t[onInds]
onSamplesInHeader=int(3.E0*tauc/taus) #Number of digitizer samples expected to be high in header.
onSamplesInCloser=int(2.E0*tauc/taus) #Number of digitizer samples expected to be low in closer.
codeLength=int(dt/taus) #Number of samples expected in whole code.

#Find pairs of times/indices wherein the time separating two
#adjacent time points where the signal is ON is greater than
#the duration of an encoded logic bit pattern.  These mark the
#times dividing the short periods of encoded signal and the long
#periods of no signal.
#The "WithinOnInds" designation implies that these are indices
#into the array of indices that the signal is on.
#endIndsWithinOnInds = find( diff( onTimes ) > 1.05*dt ) #Found that this sometimes lumped two encoded signals together.
#endIndsWithinOnInds = find( diff( onTimes ) > 0.85*dt )

#endIndsWithinOnInds = find( diff( onTimes ) > dt-(tbin+2.E0*tbin/3.E0)*0.75 ) # Off time must be bigger than space between header and closer on times.
#startIndsWithinOnInds = add(endIndsWithinOnInds,1)

#Find header sample indices
headInds=[]
closeInds=[]
ii=0
while ii < len(y) :
	if(all(y[ii:ii+onSamplesInHeader]>1.0E0)) : #Header found - store and jump to end of code.
		headInds.append(ii)
		ii=ii+codeLength-onSamplesInCloser-3
		continue
	elif(all(y[ii:ii+onSamplesInCloser]>1.0E0)) :
		closeInds.append(ii) #Start index of closer found - store.  Code is between these two indices.
		ii=ii+onSamplesInCloser-3
	ii=ii+1 #Increment index

#headInds=find( [all(y[ii:ii+onSamplesInHeader]>1.0E0) for ii in range(0,len(y)) ] )
#Find closer sample indices
#closeInds=find( [all(y[ii:ii+onSamplesInCloser]>1.0E0) and ~all(y[ii:ii+onSamplesInHeader]>1.0E0) for ii in range(0,len(sy)) ] )

#The first time with an "ON" value marks the ON time of the first encoded signal.
#Likewise, the last "ON" value marks the OFF time for the last encoded signal.
#However, these will not be found in the lines of code above, since that code looks
#for the long periods of OFF time between encoded signals.  Add them below.

#startIndsWithinOnInds=insert(startIndsWithinOnInds, 0, 0)
#endIndsWithinOnInds=append( endIndsWithinOnInds, len(onInds)-1 )

#assert_stmt ::=  "assert" len(startIndsWithinOnInds)==len(endIndsWithinOnInds)
codeVals=zeros(len(closeInds)) #Preallocate array

# Takes an array containing a list of bits which are on in a binary number, in any order, with least-significant value corresponding to 0, and returns the decimal number corresponding to this number.
def onBits2num(bitInds) :
	if len(bitInds)==0 : return 0
	else : return sum([ pow(2,aa) for aa in bitInds ])

#Loop through all indices containing the start and end times for encoded bit patterns
for i in range( 0, len(closeInds) ) :
#for i in range( 0, 1 ) :
	#bitNum = 
	#Within each encoded segment, divide up the segment into bins of duration, tbin.
	#The state of the bits are contained in each bin.  Find and number the bins for which the
	#board output was high.
	#tOnInBin=subtract( onTimes[startIndsWithinOnInds[i]:endIndsWithinOnInds[i]+1],onTimes[startIndsWithinOnInds[i]] )
	tOnInBin= t[headInds[i]+find( y[headInds[i]:closeInds[i]]>1.E0 )] - t[headInds[i]]
	tOnInBin= tOnInBin[find([tOnInBin[ii]>2.E0*tbin and tOnInBin[ii]<(2.E0+nbits)*tbin for ii in range(0,len(tOnInBin))])]
	tOnInBin=tOnInBin-2.E0*tbin #Subtract time equivalent to first two time bins from signal - these are for the header.

	#onBins = unique([ int(aa) for aa in divide( subtract( onTimes[startIndsWithinOnInds[i]:endIndsWithinOnInds[i]+1],onTimes[startIndsWithinOnInds[i]] ), tbin ) ])
	onBins = unique([ int(aa) for aa in divide( tOnInBin, tbin ) ])
	#The first two bins (i.e t>0 and t < 2*tbin) comprise the header; the last bin comprises the closer.
	#Remove these bins from consideration.  The remaining internal bins comprise the logic signal,
	#ordered most-to-least significant bit.  Turn these numbers into the 2's place to simplify conversion
	#into a decimal number.
	#In the header, only the first bin has an on signal.  The second does not.
	#onBits = subtract((nbits - 1), subtract(onBins[1:-1],2))
	#onBits = (nbits - 1) - (onBins[1:-1]-2)
	onBits = (nbits - 1) - onBins #(Already took out header and closer)
	print(onBits)
	#Convert array showing which places are 1 in the binary number into a decimal number.  Store.
	codeVals[i] = onBits2num(onBits)

#plot(t[onInds[startIndsWithinOnInds[i]]:onInds[endIndsWithinOnInds[i]]+1],y[onInds[startIndsWithinOnInds[i]]:onInds[endIndsWithinOnInds[i]]+1])
#plot(t[headInds[0]:headInds[0]+codeLength], y[headInds[0]:headInds[0]+codeLength] )

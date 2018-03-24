from numpy import *
import pdb

def myRfft(y, t) :
	"""
	This function wraps the numpy function, rfft, in a tool which will also compute and put out the frequency axis
	corrresponding to the discrete Fourier transform.

	Usage:
		[Y,f] = myRfft(y,t)

	Input:
	@param y Purely-real input signal
	@param t Time axis of input signal OR sample time (1/sample frequency) of input if length=1

	Output:
	@return [Y,f]; Y=output from rfft = real fast Fourier transform; f=frequency axis [1/time unit]

	Note that the output of Y will work with the pure numpy function, irfft

	Ted Golfinopoulos, 3 Feb 2012
	"""

	if (len(t)==1) :
	    df = 1.E0/t #Sampling frequency given as argument instead of time vector.
	else :
	    dt = abs(t[1] - t[0]) #Sampling time from time axis
	    df = 1.E0 / dt #Upper/lower frequency (absolute value) bounds of dft

	Y=fft.rfft(y) #Compute real fast Fourier transform
	
	f=(df/2.E0)*linspace(0.E0,1.E0,len(Y)) #Compute frequency axis.  Divide df by 2 because we are only looking at the positive frequencies, since the input is known real, and so the frequency extent is from 0 to df/2, instead of -df/2 to df/2.

	return [Y, f]

f=1.E0 #Frequency [Hz]
omega=2*pi*f
tau=1.E0/f
t=linspace(0,3*tau,500)
y=cos(omega*t)
Y,f=myRfft(y,t)

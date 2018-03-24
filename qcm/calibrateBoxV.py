from myRfft import *
import pdb
from numpy import interp,concatenate,load
from numpy import fft

def calibrateFourierDomain( y, t, Hc, fc ) :
    """
    This function accepts a time-domain signal as input, applies a Fourier-domain calibration via the given Fourier domain transfer function, and returns the 
calibrated time-domain signal.

    USAGE:
        yout = calibrateFourierDomain( y,t, Hc, fc )

    INPUT:
        y = signal in time domain.
        t = timebase for y
        Hc = transfer function in frequency domain - multiply this with the Fourier transform of y
        fc = frequency base for H

    OUTPUT:
        yout = calibrated signal in time domain, ifft( H*fft(y))

    Ted Golfinopoulos, 1 June 2013

    """

    #Compute fast Fourier transform for non-negative frequencies given that v is a real signal.
    Y,f=myRfft(y, t )

    def interpComplex(x,xp,yp) :
        """
        Interpolate for real x and complex y.
        Ted Golfinopoulos, 17 Feb 2012
        """
        return interp(x,xp, real(yp)) + 1j*interp(x,xp,imag(yp))

    if(min(fc)==0.0): #If frequency response is available to 0 kHz, use this frequency response all the way to DC
        fmin=0.0
    else: #Otherwise, truncate 3 kHz above the minimum frequency to avoid corner effects - legacy
        fmin = min(fc)+3E3

    fmax = max(fc)-3E3
    #pdb.set_trace()
    #Apply calibration in-place.  Elementwise multiplcation is the default for * for numpy arrays.
    #Lock calibration at the value from 50 kHz for frequencies lower than 50 kHz, and at 300 kHz
    #for frequencies higher than 300 kHz.    
    
    Hfmin=interpComplex(fmin, fc, Hc)#Calibration at fmin
    Hfmax = interpComplex(fmax, fc, Hc) #Calibration at fmax

    lowFreq=Hfmin*ones(sum(f<=fmin)) #Fix calibration for frequencies < fmin, since calibration is not available for lower frequencies.
    midFreq=interpComplex(f[(f>fmin) * (f<fmax)],fc,Hc)

    #midFreq=interp(f[(f>50.E3) * (f<300.E3)],fc,real(Hc))+1j*interp(f[(f>50.E3) * (f<300.E3)],fc,imag(Hc)) #Concatenate variable calibration for intermediate frequencies.
    highFreq=Hfmax*ones(sum(f>=fmax)) #Concatenate fixed calibration for frequencies over fmax kHz.
    scaleFac=concatenate((lowFreq,midFreq,highFreq))

    print('Calibration factor calculated.')

    Y=Y*scaleFac

    print('Transformed signal calibrated - getting ready to invert transform.')
    #Invert Fourier transform and return.
    return fft.irfft(Y)

def calibrateBoxV( v, t, boxID, calibType='voltage') :
    """
    #calibrateBoxV.py
    #Function to apply frequency-dependent calibration to I/V Box voltage.  The calibration was found from comparison of         #the box output voltage to that from a 10:1 scope probe, with a sweeping-frequency input and a digital 'scope.
    #
    #USAGE:
    #
    #vout = calibrate( v, t, boxID[, calibTybe] )
    #
    #INPUT
    #v = raw, real-valued output voltage from IV probe box
    #t = timebase for probe box voltage
    #boxID = number of probe box (1, 2, or 3)
    #calibType = string input specifying whether to calibrate voltage or current signal.  Default=voltage.  For current, input 'current'
    #
    #OUTPUT
    #vout = calibrated voltage.
    #
    #Ted Golfinopoulos, 3 Feb 2012
    """

    if(boxID<1 or boxID>4) :
        print("Input error: boxID label must be 1, 2, 3, or 4.  Defaulting to boxID=1")
        boxID=1

    print('Calibrating data for Box {0:d}'.format(boxID))

#    print('FFT calculated')

    #Load calibration binary files.  sd=>synchronous detection method; sp=>spectrogram method.
    #Grab data for relevant I/V box
    path='/home/golfit/python/versionControlled/trunk/qcm/'
    if(boxID>=1 and boxID<=3) :
        nameExt="Box{0:d}".format(boxID)
        #Hc=load(path+"HsdS"+nameExt) #Sync. detect.
        #fc=load(path+"fsdS"+nameExt)
        #Spectrogram method seems a little more reliable <60 kHz, so try Hsp instead of Hsd.
        HcName=path+"HspS"+nameExt
        fcName=path+"fspS"+nameExt
        fmin=45.E3 #Minimum frequency for which calibration is available
        fmax=300.E3 #Maximum frequency for which calibration is available
    else : #boxID=4 - Isolation box calibration.
        HcName=path+'HisoCalib'
        fcName=path+'FisoCalib'
        fmin=5.E3 #Minimum frequency for which calibration is available
        fmax=305.E3 #Maximum frequency for which calibration is available

    #Choose whether calibration of current or voltage signals.
    if(calibType=='current') :
        HcName=HcName+'i.npy'
        fcName=fcName+'i.npy'
    else :
        HcName=HcName+'.npy'
        fcName=fcName+'.npy'

    Hc=load(HcName)
    fc=load(fcName)

    print('Loaded '+HcName)

    return calibrateFourierDomain(v,t,Hc,fc)

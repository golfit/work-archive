from MDSplus import *
from decodeSignal import *
from myToolsNoSql import parseList, lp, hp, bp, getYX
import numpy
import scipy
import scipy.signal
import sys
import time
import re
#import pickle

#T. Golfinopoulos, 1 April 2016

#sList=parseList(int(sys.argv[1])) #0th argument is script name; first argument is shot number.  Parse integer.
sList=[int(sys.argv[1])] #Getting error in this - skip for now

def getTSlow( t_orig, fs_slow=5000 ):
    '''
    Generate slower timebase from original.
    
    USAGE:
        getTSlow( t_orig, fs_slow=5000 )
    
    INPUT:
        @param t_orig = original timebase vector [s]
        @param fs_slow = sampling frequency of new timebase [Hz].  Optional parameter.  Default=5000 Hz
    
    OUTPUT:
        @return t_slow = timebase with fs_slow sampling frequency. [s]
    
    Ted Golfinopoulos, 1 April 2016 (April Fools' Day)
    '''
    
    fs=1.0/(t_orig[1]-t_orig[0]) #Sampling frequency of original timebase
    
    step_inds=round(fs/fs_slow) #Step size for downsampled timebase (in index)
    ind1=int(round(0.5*fs/fs_slow))-1
    t1=t_orig[ind1]
    
    nsteps=int(floor((len(t_orig)-ind1)/step_inds))
    ind2=round(ind1+nsteps*step_inds)

    t2=t_orig[ind2]
    
    return numpy.linspace(t1,t2,nsteps) #numpy.arange(t1,t2,1.0/fs_slow)

def getPwr(y1,y2,fs,fs_slow=5000):
    '''
    This function computes the cross-power of two signals using synchronous detection:
    
    USAGE:
        getPwr(y1,y2,fs)
        
    INPUT:
    
    OUTPUT:
        (1/2)*lp{hp{y1}*hp{y2}}
        
        A1*cos(wt+a1)*A2*cos(wt+a2)
        
        = A1*A2*( cos(wt)*cos(a1)-sin(wt)*sin(a1) ) * ( cos(wt)*cos(a2)-sin(wt)*sin(a2) )

        = A1*A2 * ( cos^2(wt)*cos(a1)*cos(a2) - cos(wt)*sin(wt)*cos(a1)*sin(a2) - cos(wt)*sin(wt)*sin(a1)*sin(a2) + sin^2(wt)*sin(a1)*sin(a2) )

        After smoothing,
        
        cos^2(wt) = (1+cos(2wt))/2 -> 1/2,
        sin^2(wt) = (1-cos(2*w*t))/2 -> 1/2

        = A1*A2*(cos(a1+a2) + cos(a1-a2) + cos(a1-a2) + cos(a1-a2) - cos(a1+a2) )/4
        =A1*A2*cos(a1-a2)/2
        
        =(1/2)*Re{ Y1 * Y2'}, as expected

        cos(a+b)=cos(a)*cos(b)-sin(a)*sin(b)
        
        Amplitude of A
    '''
    
    fc_low=0.4*fs_slow #Filter out freq. components a freq. slightly below Nyquist freq. of slower signal
    fc_high=5.0*fc_low #Put distance between low- and high-pass filtering
    
    if(y1 is y2): #If y1 and y2 are the same, only perform high-pass filter step once.
        y1HP=hp(y1,fs,fc_high)
        pwr=lp(y1HP*y1HP,fs,fc_low)
    else:
        pwr=lp(hp(y1,fs,fc_high)*hp(y2,fs,fc_high),fs,fc_low)
    
    #Downsample pwr signal, keeping backwards compatibility in downsampling style
    #Note: pwr should be numpy array for slicing via list of integers
    step=int(round(fs/fs_slow))
    ind1=int(round(0.5*fs/fs_slow)-1)
    nsteps=int(floor((len(y1)-ind1)/step))
    ind2=int(nsteps*step)
    
    return pwr[list(range(ind1,ind2,step))]

def getCrossPwr(y1,y2,fs,fs_slow=5000):
    '''
    Calculate cross-power between two signals in the time-domain via synchronous detection
    
    USAGE:
        getCrossPwr(y1,y2,fs,fs_slow=5000)
    
    INPUTS:
        @param y1 = first signal to process
        @param y2 = second signal to process
        @param fs = sampling frequency of y1 and y2
        @param fs_slow = sampling frequency of down-sampled cross-power.  Optional input.  Default=5000 Hz.
        
    OUTPUT:
        @return pxy = Cross power - complex-valued array down-sampled with sampling frequency, fs_slow.
                    The phase angle is angle(y1)-angle(y2), for Y1*Y2', ' representing the complex conjugate.
                    

    T. Golfinopoulos, 1 April 2016
    '''
    
    #If y1 and y2 are the same vector, zero phase difference - don't calculate Hilbert transform
    if(y1 is y2) :
        return getPwr(y1,y2,fs,fs_slow)

    fc_low=0.4*fs_slow #Filter out freq. components a freq. slightly below Nyquist freq. of slower signal
    fc_high=5.0*fc_low #Put distance between low- and high-pass filtering
    
    cpHigh=hp(y1,fs,fc_high)*numpy.conjugate(scipy.signal.hilbert(hp(y2,fs,fc_high)))
    crossPwr=lp(numpy.real(cpHigh),fs,fc_low)+1j*lp(numpy.imag(cpHigh),fs,fc_low)
    
    #Down-sample onto timebase with sampling frequency, fs_slow 
    #Note: pwr should be numpy array for slicing via list of integers
    step=int(round(fs/fs_slow))
    ind1=int(round(0.5*fs/fs_slow)-1)
    nsteps=int(floor((len(y1)-ind1)/step))
    ind2=int(nsteps*step)
    
    return crossPwr[list(range(ind1,ind2,step))]
    
def getZ(y1,y2,fs,fs_slow=5000):
    '''
    Get transfer function, or complex impedance, Z=y1/y2
    
    USAGE:
        getZ(y1,y2,fs,fs_slow=5000)
    
    INPUTS:
        @param y1 = numerator, "voltage"
        @param y2 = denominator, "current"
        @param fs = sampling frequency, y1 and y2
        @param fs_slow = slower sampling frequency on which to resample transfer function.  Optional input.  Default=5000 Hz
    
    OUTPUTS:
        @return Z = complex transfer function, or impedance, down-sampled onto slower sampling frequency, fs_slow
    
    T. Golfinopoulos, 1 April 2016

    '''
    
    crossPwr=getCrossPwr(y1, y2, fs, fs_slow)

    return crossPwr/getPwr(y2,y2,fs,fs_slow)
    
        
def getAmp(y,fs,fs_slow=5000) :
    '''
    This function calculates the amplitude of a signal and downsamples onto a slower timebase.
    
    USAGE:
        getAmp(y,fs,fRes=5000)
        
        @param y = signal to process
        @param fs = sampling frequency of signal [Hz].  If len(y)=length(fs)>1, then it is assumed that fs is actually time axis, t, and fs is calculated as fs=1/(t[1]-t[0])
        @param f_res = desired frequency resolution.  Optional argument.  Default=5000 Hz
    
    RETURNS:
        y_amp - time-series amplitude of y, downsampled to 1/1000 the original sampling time for
                backwards compatibility.
    
    T. Golfinopoulos, 31 March 2016
    '''
    
    #Get autopower of y 
    y_pwr=getPwr(y,y,fs,fs_slow)
    
    #Scale autopower of y appropriately and take square root to return amplitude.    
    return numpy.sqrt(2*abs(y_pwr))
    
def thisSmooth( y, N=5) :
    '''
    N-point running average smoothing.  Uses numpy.convolve
    
    USAGE:
        thisSmooth( y, N=5 )
    
    INPUTS:
        @param y = signal to smooth
        @param N = number of points smoothed in running average.  Optional input.  Default value=5.
    
    OUTPUTS:
        @return y_smooth = result of N-point running average.  Length of y_smooth is the same as length of y.
    
    T. Golfinopoulos, 1 April 2016
    '''
    
    return numpy.convolve(y, numpy.ones((N,))/N, 'same')

def getFreq(y,t,t_slow, y_thresh=2.5):
    '''
    Decode frequency from sync signal.
    
    USAGE:
        getFreq(y,t,fs_slow=5000, y_thresh=2.5)
        
        @param y = TTL signal encoding the "sync" signal, with rising edges showing the the start of periods
        @param t = timebase associated with y
        @param t_slow = slower timebase on which to sample frequency
        @param y_thresh = threshold value separating logical HIGH and LOWs.  Optional input, default=2.5 V.
        
        Note: signal must have at least 500 elements.
    RETURNS:
        @return f = frequency time series on default time 
        
    T. Golfinopoulos, 31 March 2016
    '''
    
    #Find rising edges
    risingInds=numpy.where(numpy.diff(numpy.double(numpy.array(y>y_thresh)))>0)
    fallingInds=numpy.where(numpy.diff(numpy.double(numpy.array(y>y_thresh)))<0)
    t_freqs=t[risingInds]
    periods=numpy.diff(t_freqs)
    freqs=1.0/periods #Calculate frequency from time delay between rising edges
#    t_slow=numpy.linspace(t[499],t[-500],numpy.round( (t[-1]-t[0])*fs/1000 ))
    N=5 #Average frequency over five samples to mitigate +1 errors
    f=numpy.interp(t_slow, t_freqs[0:-1], thisSmooth(freqs, N)) #Interpolate frequencies onto downsampled time grid
    
    return f #Return frequency time series



def thisPutData( y, to_node):
    '''
    Convenience function to drop processed signal into signal node and point timebase to slow timebase node.
    
    USAGE:
        thisPutData( y, to_node)
    
    INPUT:
        @param y = time series vector to drop into signal node 
        @param to_node = signal node in tree into which y should be dropped
    
    OUTPUT:
        none
    
    SIDE EFFECTS:
        prints to screen
    
    T. Golfinopoulos, 1 April 2016
    '''
    #print(numpy.real(y))
    #to_node.putData(Data.compile('Build_Signal($VALUE,$1,\MAGNETICS::TOP.SHOELACE:T_SLOW)', numpy.sign(numpy.real(y))*abs(numpy.real(y))))
    to_node.putData(Data.compile('Build_Signal($VALUE,$1,\MAGNETICS::TOP.SHOELACE:T_SLOW)', thisSmooth(numpy.real(y))))
    #to_node.putData(Data.compile('Build_Signal($VALUE,$1,\MAGNETICS::TOP.SHOELACE:T_SLOW)', numpy.real(y)))
    #print(to_node.getData().evaluate().data())
    print(' '+time.strftime(time.asctime())+" - Put processed data into "+str(to_node.getFullPath())) #Timestamp at end of program execution
    
def procAmp( from_node, to_node ):
    '''
    This function pulls data, calculates the amplitude, and pushes the processed data.
    
    USAGE:
        procAmp( from_node, to_node )
        
    INPUT:
        @param from_node = node from which data should be pulled and amplitude calculated
        @param to_node = node into which processed amplitude should be dropped
    
    OUTPUT:
        none
    
    SIDE EFFECTS:
        prints to screen informing on status
    
    T. Golfinopoulos, 1 April 2016
    '''
    (y,t)=getYX(from_node)
    y_amp=getAmp(y, fs)
    t_amp=getTSlow(t)
    
    thisPutData(y_amp, to_node)

def processVI(V_node,I_node,fs_slow=5000):
    '''
    Process pair of nodes, voltage and current.  Calculate amplitudes, impedance, and power for the pair.  Store in tree.
    
    USAGE:
        processVI(V_node,I_node,fs_slow=5000):
    
    INPUTS:
        @param V_node = MDSplus signal node pointing to voltage waveform
        @param I_node = MDSplus signal node pointing to current waveform
        @param fs_slow = slower sampling frequency on which to resample transfer function.  Optional input.  Default=5000 Hz
        
    OUTPUTS:
        none
    
    SIDE EFFECTS:
        prints concerning status of calculation
    
    T. Golfinopoulos, 1 April 2016
    '''
    
    #Pull data
    (V,t)=getYX(V_node) #Voltage waveform
    I=I_node.getData().evaluate().data() #Current waveform
    fs=1.0/(t[1]-t[0]) #Sampling frequency
    
    myTree=V_node.getTree()
    
    #Calculate current autopower and amplitude
    I_pwr=getPwr(I,I,fs,fs_slow)
    I_amp=sqrt(2.0*abs(I_pwr))
    
    #Calculate voltage amplitude
    V_amp=getAmp(V,fs,fs_slow)
    
    #Calculate cross power
    Pxy=getCrossPwr(V, I, fs, fs_slow)
    
    #Calculate impedance (or transfer function)
    Z=Pxy/abs(I_pwr)
    
    #Calculate dissipated power from cross power 
    pwr=numpy.real(Pxy)
    
    #Generate node names where data is pushed from names of voltage and current nodes
    this_prefix=re.findall('(.*)_v',str(V_node.getNodeName()).lower())[0]
    
    #Store voltage amplitude
    thisPutData(V_amp, myTree.getNode('shoelace.'+this_prefix+'_v_amp'))
    #Store current amplitude
    thisPutData(I_amp, myTree.getNode('shoelace.'+this_prefix+'_i_amp'))
    #Store power time series
    #if(this_prefix.lower()=='src'):
    #    thisPutData(pwr, myTree.getNode('shoelace.'+this_prefix+'_pwr_tst'))
    #    myFile=open('src_pwr_data.p','w')
    #    pickle.dump(pwr,myFile)
    #else :
    thisPutData(pwr, myTree.getNode('shoelace.'+this_prefix+'_pwr'))
    #Store impedance time series
    thisPutData(numpy.real(Z), myTree.getNode('shoelace.'+this_prefix+'_zr'))
    thisPutData(numpy.imag(Z), myTree.getNode('shoelace.'+this_prefix+'_zi'))
    #There may or may not be a reflected power node - try to add, and if can't skip and move on.
    try :
        rho_node=myTree.getNode('shoelace.'+this_prefix+'_rho') #Grab node into which absolute value of refl. coef goes.
        Z0=50.0 #Assume characteristic impedance of transmission line is 50 ohms
        Gamma=(Z-Z0)/(Z+Z0) #Calculate reflection coefficient
        thisPutData( abs(Gamma), rho_node)
    except :
        print('  -rho node may not exist for '+this_prefix)

################################################    
#Main part of script, organizing all processing#
################################################

print("Begin Shoelace Antenna Power System Processing: "+time.strftime(time.asctime())) #Timestamp at start of program execution

#Process all shots in list
for s in sList :
    myTree=Tree('magnetics',s)
    t=myTree.getNode('shoelace.timebase').getData().evaluate().data()
    vco_sync=myTree.getNode('shoelace.vco_sync').getData().evaluate().data()
    fs=1.0/(t[2]-t[1]) #Sampling frequency
    
    #Calculate new timebase and store in t_slow.  Use default for slower timebase sampling frequency.
    fs_slow=5000.0
    ts_slow=1.0/fs_slow
    t_slow=getTSlow(t,fs_slow)
    #Need len(t_slow)-1 because this is the last index (with 0 index convention) of the timebase.
    myTree.getNode('shoelace.t_slow').putData(Data.compile('Build_Dim(Build_Window(0, $1, $2), * : * : $3)', len(t_slow)-1, t_slow[0], ts_slow ))
    
    #Calculate VCO frequency from sync signals and store in tree
    thisPutData( getFreq(vco_sync,t,t_slow), myTree.getNode('shoelace.vco_freq') )
    
    #Calculate amplitudes of voltage and current waveforms, power, and impedance for voltage and current pairs
    processVI(myTree.getNode('shoelace.src_v'),myTree.getNode('shoelace.src_i'))
    processVI(myTree.getNode('shoelace.src2_v'),myTree.getNode('shoelace.src2_i'))
    processVI(myTree.getNode('shoelace.ant_v'),myTree.getNode('shoelace.ant_i'))
    processVI(myTree.getNode('shoelace.match_v'),myTree.getNode('shoelace.match_i'))

print("End: "+time.strftime(time.asctime())) #Timestamp at end of program execution

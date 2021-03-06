#This script calibrates the Mirnov coils using the complex calibration factors stored in the tree.
#Ted Golfinopoulos, 26 August 2015.

import sys
from MDSplus import *
from calibrateBoxV import calibrateFourierDomain
import myTools_no_sql as myTools
from myTools_no_sql import getYX
#import numpy
import time
import re
from scipy.signal import freqs
from math import pi
from myRfft import *
from numpy import fft

sList=myTools.parseList(sys.argv[1]) #Get shot from command line, first argument
#sList=[1150826028] #This shot had a disruption - use for testing.
#sList=[1150820004] #This shot had a fizzle - use for testing
elimTags=['OLD','_K$','ASP']

def getDigiNum(sigNode) :
    #Parse digitizer number from expression in node.

    try :
        #First, check if node has a subnode called raw:
        digiNum=re.findall( 'acq_216_(\d)', str(sigNode.getNode('raw').getData().decompile()).lower())
    except :
        #Otherwise, try to parse digitizer number from signal
        digiNum=re.findall( 'acq_216_(\d)', str(sigNode.getData().decompile()).lower())

    if not all([digiNum[0]==digiNum[i] for i in range(0,len(digiNum))]) :
        print("Error in "+str(sigNode.getFullPath())+" - multiple digitizers apparently referenced in node.  Skipping.")
#        continue
    elif len(digiNum)==0:
        print("Could not find digitizer number for "+str(sigNode.getFullPath())+" - skipping")
#        continue

    #Multiple occurrences of the digitizer path may occur - isolate the number from the list returned by findall.
    print(digiNum)
    print(str(sigNode.getFullPath()))
    digiNum=digiNum[0]
    return digiNum

for s in sList :	
    #Open tree
    myTree=Tree('magnetics',s)

    topNode=myTree.getNode('active_mhd.signals')

    #Get sub-nodes referring to Mirnov coils
    mirnovNodes=myTree.getNode('active_mhd.signals').getNodeWild('BP*')
    
    print('Start Time: '+time.asctime())
    tStart=time.time()
    for n in mirnovNodes :
        if(not(any([re.match('.+'+elimTag,str(n.getFullPath())) for elimTag in elimTags])) and n.isOn()) :
            calibDone=False
            try :
                #Fetch signal to be calibrated - note that the calibration factor applies to the old signal expression, with units of T/s
                y,t=getYX(n.getNode('raw'))
                Hnum=n.getNode('H_NUM').getData().evaluate().data()
                Hden=n.getNode('H_DEN').getData().evaluate().data()
                fScale=n.getNode('F_SCALE').getData().evaluate().data()
                
                #Compute fast Fourier transform for non-negative frequencies given that v is a real signal.
                Y,f=myRfft(y, t )
                #Try to use polynomial fit to H
                w,H=freqs(Hnum,Hden,f*2.0*pi/fScale)
                #Limit max value of H, as inverse of coil response blows up at high frequency
                #if(s<1160000000) : #Higher frequency scan in 2016 calibration.
                #    fMax=1.35E6 #Maximum frequency in response - fix after that.                
                #else :
                #    fMax=1.25E6 #Maximum frequency in response - fix after that.
                fMax=1.5E6
                Hlim=100.0
                wmax,Hmax=freqs(Hnum,Hden,fMax*2.0*pi/fScale)
                H[f>fMax]=Hmax #Note: this ensures that H is no longer causal - for Mirnov coils, this is already the case.
                H[H>Hlim]=Hlim*H/abs(H) #Cap maximum scaling factor for coils that diverge too rapidly in inverted response.
                print('Hmax='+str(abs(Hmax)))
                #Apply calibration in frequency domain and invert the Fourier transform under the assumption that y is real
                ycal=fft.irfft(Y*H)
                calibDone=True
                print(str(s)+': finished calibrating '+str(n.getFullPath())+' using rational polynomial fit to coil system response')
            except :
                try :
                    print('getSig')
                    #Fetch calibration from tree
                    print('get real')
                    Hreal,fAxis=getYX(n.getNode('H_real'))
                    print('get imag')
                    Himag=getYX(n.getNode('H_imag'))[0]
                    H=Hreal+1j*Himag
                    
                    #Compute calibrated value of signal
                    ycal = calibrateFourierDomain(y,t,H,fAxis)
                    
                    calibDone=True
                    print(str(s)+': finished calibrating '+str(n.getFullPath()))
                except :
                    print('Cannot calibrate '+str(n.getFullPath())) #Skip if can't calibrate
            
            if calibDone :
                #Store calibrated value in tree
                #Parse digitizer and point to appropriate timebase.
                digiNum=getDigiNum(n)
                #The calling sequence, Data.compile(myTdiStr), was broken by an "improvement" to MDSplus around 6 Oct. 2017
                n.getNode('calib').putData(myTree.tdiCompile('Build_Signal($VALUE,$1,'+str(myTree.getNode('active_mhd.signals.timebase'+str(digiNum)).getFullPath())+')',ycal))
                
                n.putData(myTree.tdiCompile(str(n.getNode('calib').getFullPath())))
                    
    print('Finished calibrating '+str(s)+', elapsed time='+str(int((time.time()-tStart)*1000)/1000.0)+' s')

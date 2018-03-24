#This script writes Mirnov coil calibration data to corresponding nodes.
#1150319900-905
#
#Ted Golfinopoulos, 13 May 2015
#Modified 28 Sep. 2017 - use 2015 calibration for 2015 campaign and earlier, and 2016 calibration for 2016 campaign

from MDSplus import *
from myTools import *
import myTools
from numpy import abs, angle, imag, real, array
import re #For regular expressions
import scipy.io as sio
from numpy import mean
from numpy import pi
import time
import re #Regular expressions

#s=-1 #1150825900 #1150513912 #This is a test shot in which we will populate the initial attempts to populate the tree before making changes to the model tree.
#s=1150826028 #This shot had an early disruption - use for testing
#s=1150820004 #This shot had a fizzle - use for testing
#s=1150716033 #Seung-Gyou Baek wanted to analyze this shot for toroidal mode numbers from the Mirnov coils.
#s=1150722020 #Seung-Gyou Baek wanted to analyze this shot for toroidal mode numbers from the Mirnov coils.
sList=myTools.parseList(sys.argv[1]) #Get shot from command line, first argument

elimTags=['OLD','_K$','ASP']

path_to_calib2015='/home/golfit/matlab/laptop/work/MirnovCoils/Calib2015Fix2017/'
path_to_calib2016='/home/golfit/matlab/laptop/work/MirnovCoils/Calib2016Fix2017/'

#calib_shot=1150319900 #Calibration shot from which data is used.

#Step through nodes and add calibration nodes under each Mirnov coil
# ~/matlab/laptop/work/MirnovCoils/Calib/Bp_ef_topCalibFactorAveraged
        #Calibate to field measurement averaging over lowest 5 kHz, eliminating first datapoint due to unreliability.  Assume that low-frequency measurement is calibrated by coil NA product in tree.
    #Hsp=calibDat["Hsp"]
    #fsp=calibDat["fsp"]
    #fRange=5.0E3
    #fRange=1E3
    #ind2=find
    #myInds=fsp>fsp[0] and fsp<(fsp[1]+fRange)
    #Hsp0=mean(Hsp[myInds]/(2.0*pi*fsp[myInds]))
    #B0=Hsp0/
        

for s in sList :
    print("Processing "+str(s))
    #Open tree
    myTree=Tree('magnetics',s)

    topNode=myTree.getNode('active_mhd.signals')
    
    time_now=time.localtime()
    if(s<1160000000):
        path_to_calib=path_to_calib2015
        #Formerly, calibration shot range was 1150319900-905
        commentStr='Mirnov calibration data averaged from 1150319900-1150319905, used to generate transfer function, H.  \nSignals store the magnitude (H_MAGNITUDE), phase (H_PHASE), real (H_REAL), and imaginary (H_IMAG) parts of the transfer function, \ntabulated on the frequency base, freq_axis, in Hz.  The transfer function is dimensionless ([T/T]), and corresponds to the vacuum dipole field \nintercepted by the Mirnov coil divided by the nominal field measurement made by the coil at each frequency.  The transfer function should \nbe multiplied with the Fourier transform of the associated Mirnov coil signal, and the product inverse transformed back to the time domain.\nH_NUM and H_DEN are the coefficients for the numerator and denominator of rational polynomial fit the the transfer function, specified as\n(H_NUM[0]*s^7+H_NUM[1]*s^6+...+H_NUM[7])/(H_DEN[0]*s^7+H_DEN[1]*s^6+...+H_DEN[7]),\nwhere s is scaled by 1/F_SCALE (i.e. frequencies are divided by this amount).\nCalibration updated on '+str(time_now[0])+"."+str(time_now[1])+"."+str(time_now[2])+","+str(time_now[3])+":"+str(time_now[4])
    else:
        path_to_calib=path_to_calib2016
        commentStr='Mirnov calibration data averaged from 1160221900-1160221905, used to generate transfer function, H.  \nSignals store the magnitude (H_MAGNITUDE), phase (H_PHASE), real (H_REAL), and imaginary (H_IMAG) parts of the transfer function, \ntabulated on the frequency base, freq_axis, in Hz.  The transfer function is dimensionless ([T/T]), and corresponds to the vacuum dipole field \nintercepted by the Mirnov coil divided by the nominal field measurement made by the coil at each frequency.  The transfer function should \nbe multiplied with the Fourier transform of the associated Mirnov coil signal, and the product inverse transformed back to the time domain.\nH_NUM and H_DEN are the coefficients for the numerator and denominator of rational polynomial fit the the transfer function, specified as\n(H_NUM[0]*s^7+H_NUM[1]*s^6+...+H_NUM[7])/(H_DEN[0]*s^7+H_DEN[1]*s^6+...+H_DEN[7]),\nwhere s is scaled by 1/F_SCALE (i.e. frequencies are divided by this amount).  \nCalibration updated on '+str(time_now[0])+"."+str(time_now[1])+"."+str(time_now[2])+","+str(time_now[3])+":"+str(time_now[4])

    #Get sub-nodes referring to Mirnov coils
    mirnovNodes=myTree.getNode('active_mhd.signals').getNodeWild('BP*')
    #print(mirnovNodes)
    for n in mirnovNodes :
        if(not(any([re.match('.+'+elimTag,str(n.getFullPath())) for elimTag in elimTags])) and n.isOn()) :
            try :
                #Pull calibration data.
                myNodeName=str(n.getNodeName())
                myNodeName=myNodeName[0].upper()+myNodeName[1:].lower()
                calibName=path_to_calib+myNodeName+"CalibFactorAveraged.mat"
                calibData=sio.loadmat(calibName)
                #Write data  to tree.
                H=calibData['avgCalibFactor'][0]
                avgHNum=calibData['avgHnum'][0]
                avgHDen=calibData['avgHden'][0]
                fScale=calibData['fScale'][0]
                #Magnitude of transfer function.  Dimensionless
                #The calling sequence, myNode.putData(Data.compile(myTdiStr)), was broken by an "improvement" to MDSplus around 6 Oct. 2017
                n.getNode('H_MAGNITUDE').putData(myTree.tdiCompile('Build_Signal($VALUE,$1,'+n.getFullPath()+'.freq_axis)',array(abs(H))))
                #Phase of transfer function in radians
                n.getNode('H_PHASE').putData(myTree.tdiCompile('Build_Signal($VALUE,$1,'+n.getFullPath()+'.freq_axis)',array(angle(H))))
                n.getNode('H_IMAG').putData(myTree.tdiCompile('Build_Signal($VALUE,$1,'+n.getFullPath()+'.freq_axis)',array(imag(H))))
                n.getNode('H_REAL').putData(myTree.tdiCompile('Build_Signal($VALUE,$1,'+n.getFullPath()+'.freq_axis)',array(real(H))))
                #Added 3 Oct. 2017
                n.getNode('H_NUM').putData(myTree.tdiCompile('$1',array(avgHNum)))
                n.getNode('H_DEN').putData(myTree.tdiCompile('$1',array(avgHDen)))
                n.getNode('F_SCALE').putData(myTree.tdiCompile('$1',fScale))
#                for ii in range(0,len(H)) :
#                    print(real(H[ii])+"1j*"+imag(H[ii])
                n.getNode('freq_axis').putData(myTree.tdiCompile('$1',array(calibData['fAxis'][0]))) #Frequency axis against which H is is computed [Hz].
                n.getNode('comment').putData(commentStr)
            except :
                print("Error on "+str(s)+" with "+str(n.getFullPath())+ "- skipping ")
                continue
    print(" - Done")

#This script sets up the calibration nodes containing the transfer function phase and magnitude for each Mirnov coil.  These were measured on
#1150319900-905
#
#Ted Golfinopoulos, 27 May 2015
#Modified 28 Sep. 2017 to add date of calibration node setup.
#Modified 3 Oct. 2017 to add nodes for rational polynomial fits to transfer function

from MDSplus import *
from myTools import *
import myTools
import re #For regular expressions

#s=-1 #1150825900 #1150513912 #This is a test shot in which we will populate the initial attempts to populate the tree before making changes to the model tree.
#s=1150826028 #This shot had an early disruption - use for testing
#s=1150820004 #This shot had a fizzle - use for testing
#s=1150716033 #Seung-Gyou Baek wanted to analyze this shot for toroidal mode numbers from the Mirnov coils.
#s=1150722020
sList=myTools.parseList(sys.argv[1]) #Get shot from command line, first argument

elimTags=['OLD','_K$','ASP']

#Step through nodes and add calibration nodes under each Mirnov coil
for s in sList :
    print("Processing "+str(s))
    #Open tree for editing
    myTree=Tree('magnetics',s,'edit')

    topNode=myTree.getNode('active_mhd.signals')

    #Get sub-nodes referring to Mirnov coils
    mirnovNodes=myTree.getNode('active_mhd.signals').getNodeWild('BP*')
    for n in mirnovNodes :
        if(not(any([re.match('.+'+elimTag,str(n.getFullPath())) for elimTag in elimTags]))) :
            try :
                #Add nodes
                n.addNode('H_MAGNITUDE','signal')
                n.addNode('H_PHASE','signal')
                n.addNode('H_IMAG','signal')
                n.addNode('H_REAL','signal')
                n.addNode('freq_axis','numeric') #Frequency axis against which H is is computed
                n.addNode('raw','signal') #Pointer to raw signal
                n.addNode('calc_calib','action') #Action node to automatically calculate calibrated values.
                n.addNode('calib','signal') #Stores calibrated signal
                n.addNode('comment','text')
                
                #n.addNode('calib_fun','signal') #Computes transfer function using TDI expression.
                
                #n.getNode('comment').putData('Mirnov calibration data averaged from 1150319900-905, used to generate transfer function, H.  Signals store the magnitude (H_MAGNITUDE), phase (H_PHASE), real (H_REAL), and imaginary (H_IMAG) parts of the transfer function, tabulated on the frequency base, freq_axis, in Hz.  The transfer function is dimensionless ([T/T]), and corresponds to the vacuum dipole field intercepted by the Mirnov coil divided by the nominal field measurement made by the coil at each frequency.  The transfer function should be multiplied with the Fourier transform of the associated Mirnov coil signal, and the product inverse transformed back to the time domain.')
                n.getNode('raw').putData(n.getData()) #Copy old signal into "raw"
                
                #n.getNode('calib_fun').putData( Data.compile( '_raw='+str(n.getFullPath())+', _y=fft(_raw), build_signal(  )') )
            except :
                #print("Error on "+str(s)+" with "+str(n.getFullPath())+ "- skipping ")
                print("Can't add H data on "+str(s)+" with "+str(n.getFullPath())+ "- skipping ")
            try : #Added 3 October 2017
                #Add nodes
                n.addNode('H_NUM','numeric') #Numerator of polynomial approximation to frequency data
                n.addNode('H_DEN','numeric') #Denominator of polynomial approximation to frequency data
                n.addNode('f_scale','numeric') #Need to divide frequency by this amount for fit
                
                #n.getNode('calib_fun').putData( Data.compile( '_raw='+str(n.getFullPath())+', _y=fft(_raw), build_signal(  )') )
            except :
                print("Can't add H_fit nodes on "+str(s)+" with "+str(n.getFullPath())+ "- skipping ")

    myTree.write() #Write changes to tree
    print(" - Done")

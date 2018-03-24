#CalibrateBoxVoltages.py
#This script reads raw I/V box voltage data and applies the calibration routines.  It then changes the parent node references for the relevant nodes to point to the calibrated signals.

import sys
from MDSplus import *
from calibrateBoxV import calibrateFourierDomain
import myTools
import numpy

sList=myTools.parseList(sys.argv[1])

def processCalibration(parentNode,tree) :
    if(parentNode.isOn()) :
        #If there exists a node with the dc offset removed, use that; otherwise, use the raw signal.
        try :
            dataNode=parentNode.getNode('dc_removed')
        except :
            dataNode=parentNode.getNode('raw')

        #Grab data and convert to native data type
        #		print(dataNode)
        y,t=myTools.getYX(dataNode)

        print("Got data from "+str(dataNode.getPath()))

        #Calibrate
        #Grab frequency-domain calibration
        H,fc=myTools.getYX(parentNode.getNode('cal_vs_freq'))

        #Compute calibrated output
        ycal=calibrateFourierDomain(y,t,H,fc)

        #Put calibrated data into tree.
        expr=Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", ycal, t) #Build a TDI expression for storing signal
        parentNode.getNode('calibrated').putData(expr)
		
        print("Put data in "+str(parentNode.getNode('calibrated').getPath()))

        #Point node to calibrated data.
        parentNode.putData( Data.compile( str(parentNode.getNode('calibrated').getPath()) ) )
        print("Pointed parent node to calibrated node.")

    else :
        print(parentNode.getPath()+' is off - skipping.')

for s in sList :
    tree=Tree('magnetics',s)

	#Process 3 I/V boxes and the detector isolation box.
    #	nodes=list(tree.getNode('shoelace').getNodeWild('Box*')) + list([tree.getNode('shoelace.v_pickup')])
    #Process 5 I/V boxes (including spare) and the detector isolation box
    #    nodes=list(tree.getNode('shoelace').getNodeWild('*_V')) + list(tree.getNode('shoelace').getNodeWild('*_I')) + list([tree.getNode('shoelace.v_pickup')])
    #For now, don't process frequency-dependent calibration for current, since it hasn't been calibrated yet.
    nodes=list(tree.getNode('shoelace').getNodeWild('*_V')) + list([tree.getNode('shoelace.v_pickup')])

    for n in nodes :
        try :
            if(n.isOn()) :
                processCalibration(n, tree)
            else :
                print('Node '+str(n.getPath())+' is off - skipping.')
        except :
            print('Could not process node '+str(n.getPath())+' - it may not exist for this shot.  Moving on.') 
            raise

    print("Finished calibrations from Shot {0:d}".format(s))

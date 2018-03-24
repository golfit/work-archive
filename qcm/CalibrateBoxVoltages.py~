#CalibrateBoxVoltages.py
#This script reads raw I/V box voltage data and applies the calibration routines.  It then changes the parent node references for the relevant nodes to point to the calibrated signals.

import sys
from MDSplus import *
from calibrateBoxV import *
import myTools

sList=myTools.parseList(sys.argv[1])

def processCalibration(parentNode,tree) :
	if(parentNode.isOn()) :
		#If there exists a node with the dc offset removed, use that; otherwise, use the raw signal.
		try :
			dataNode=parentNode.getNode('dc_removed')
		except :
			dataNode=parentNode.getNode('raw')

		#Grab data and convert to native data type
		v=dataNode.getData().evaluate().data() #Raw voltage
		t=dataNode.getData().evaluate().dim_of().data()

		print("Got data from "+str(dataNode.getPath()))

		#Calibrate
		#Grab box ID number (1, 2, or 3 as of 20 Feb 2012) and caste as integer (native).  The casting doesn't seem necessary, but an error appears otherwise in providing to format string.
		boxID=int( parentNode.getNode('box_num').getData() )

		#Compute calibrated voltage.
		#Determine whether current signal or voltage signal.
		nPath=str(parentNode.getPath())
		
		if( nPath[-1].lower()=='i') :
			vc = calibrateBoxV(v,t,boxID,'current')
		else :
			vc = calibrateBoxV(v,t,boxID)

		#Put calibrated data into tree.
		expr=Data.compile("BUILD_SIGNAL($VALUE, $1, \MAGNETICS::TOP.SHOELACE:TIMEBASE)", vc) #Build a TDI expression for storing signal
		parentNode.getNode('calibrated').putData(expr)

		print("Put data in "+str(parentNode.getNode('calibrated').getPath()))

		#Point parent node to calibrated data.
		parentNode.putData(Data.compile(parentNode.getPath()+':CALIBRATED'))

	else :
		print(parentNode.getPath()+' is off - skipping.')

for s in sList :
	tree=Tree('magnetics',s)

	#nodePaths=['\\magnetics::top.shoelace:ant_v', '\\magnetics::top.shoelace:src_v', '\\magnetics::top.active_mhd.signals:qcm_pickup', '\\magnetics::top.shoelace:spare_v']
	#nodePaths=['\\magnetics::top.shoelace:ant_v', '\\magnetics::top.shoelace:src_v', '\\magnetics::top.shoelace:v_pickup', '\\magnetics::top.shoelace:spare_v']

	#Spare box now employed for characterizing the output from the second T&C AG1010 amplifier.
	#nodePaths=['\\magnetics::top.shoelace:ant_v', '\\magnetics::top.shoelace:src_v', '\\magnetics::top.shoelace:v_pickup', '\\magnetics::top.shoelace:src2_v', '\\magnetics::top.shoelace:spare_v', '\\magnetics::top.shoelace:ant_i']
	nodePaths=['\\magnetics::top.shoelace:ant_v', '\\magnetics::top.shoelace:src_v', '\\magnetics::top.shoelace:v_pickup', '\\magnetics::top.shoelace:src2_v', '\\magnetics::top.shoelace:spare_v']

	#Until we're verified that BOX#1 is working, we're going to use a scope probe to measure the look-in voltage (src_v).  The TDI expression,
	#SRC_V:RAW_PRB_NODC * SRC_V:CAL_PRB
	#is in \MAGNETICS::TOP.SHOELACE:SRC_V now.
	#1120502
	#nodePaths=['\\magnetics::top.shoelace:ant_v', '\\magnetics::top.shoelace:v_pickup', '\\magnetics::top.shoelace:spare_v']

	#processCalibration(tree.getNode('\\magnetics::top.shoelace:spare_v'),tree)

	for n in nodePaths :
		try :
			if(tree.getNode(n).isOn()) :
				processCalibration(tree.getNode(n),tree)
			else :
				print('Node '+n+' is off - skipping.')
		except :
			print('Could not process node '+n+' - it may not exist for this shot.  Moving on.') 
			#raise

	print("Finished calibrated voltages from Shot {0:d}".format(s))

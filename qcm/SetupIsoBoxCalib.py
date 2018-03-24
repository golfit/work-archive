#This script sets up nodes in the tree for iso box calibration.
#Ted Golfinopoulos, 28 Feb 2012

import sys #For getting command line arguments
from MDSplus import *

if(len(sys.argv)>1) :
	s=int(sys.argv[1]) #Grab shot number from command line.
else :
	s=-1 #Default to shot -1

tree = Tree('magnetics',s,'edit')

pickupNode=tree.getNode('active_mhd.signals:qcm_pickup')
pickupNode.addNode('raw','signal')
rawNode=pickupNode.getNode('raw')

rawNode.putData(Data.compile('build_signal( \magnetics::top.active_mhd.data_acq.cpci.acq_216_3:input_01, *, dim_of(\magnetics::top.active_mhd.data_acq.cpci.acq_216_3:input_01) )'))

pickupNode.addNode('box_num','numeric')

pickupNode.getNode('box_num').putData(4) #The isolation box is designated by number 4 in the calibration routine.

pickupNode.addNode('calibrated','signal')

pickupNode.addNode('comment','text')

pickupNode.getNode('comment').putData('Voltage signal induced over QCM (Shoelace) antenna.  boxNum is the designation for the isolation box used in the calibration routine.  raw=raw signal from digitizer.  calibrated=signal calibrated with isolation box transfer function.')

tree.write() #Write changes

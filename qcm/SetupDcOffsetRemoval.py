#SetupDcOffsetRemoval.py
#This script is concerned with removing the dc offset in signals associated with the shoelace antenna.  This offset seems to be present to reduce switching noise between states on the digitizer.  When there are small signals, it can affect analysis.
#Ted Golfinopoulos, 19 March 2012

import sys
from MDSplus import *
from calibrateBoxV import *

if(len(sys.argv)>1) :
	s1=int(sys.argv[1]) #Grab shot number from command line.
else :
	s1=-1 #Default to shot -1

if(len(sys.argv)>2) :
	s2=int(sys.argv[2]) #Grab shot number from command line.
else :
	s=s2 #Default to shot -1

#Add a node which holds the data less the dc offset from the digitizer as measured by the data taken during the time before the amplifier is turned on.
def setupNodes(node,pickupNode) :
	node.addNode('dc_removed','signal')
	if(pickupNode) :
		node.getNode('dc_removed').putData(Data.compile('_y='+node.getPath()+':raw, _t=dim_of('+node.getPath()+':raw), _y-mean(_y)'))
	else :
		node.getNode('dc_removed').putData(Data.compile('_y='+node.getPath()+':raw, _t=dim_of('+node.getPath()+':raw), _tStart=\\magnetics::top.shoelace:rf_gate:on, _y-mean(_y,*,_t<=_tStart)'))

	node.putData(Data.compile( node.getPath()+':dc_removed * '+node.getPath()+':cal' )) #Modify expression to point to dc_removed instead of raw.

#Add associated nodes for dc offset removal for each of the signal nodes.
#nodeNames=['ant_i', 'ant_v', 'src_i', 'src_v', 'spare_i', 'spare_v']
#nonPowerNodeNames=['v_pickup']
nodeNames=['src2_i', 'src2_v']
for s in range(s1, s2+1) :
	tree=Tree('magnetics',s,'edit') #Get the tree.

	for n in nodeNames :
		setupNodes(tree.getNode('shoelace.'+n),False)
		print("Added DC component removal nodes in "+n)

#	for n in nonPowerNodeNames :
#		setupNodes(tree.getNode('shoelace.'+n),True)
		#try :
		#	setupNodes(tree.getNode('shoelace.'+n))
		#except :
		#	print("Could not operate on shoelace."+n+" - node may not exist for the shot.  Skipping.")
#		print("Added DC component removal nodes in "+n)
	tree.write()

	print("Finished {0:d}".format(s))

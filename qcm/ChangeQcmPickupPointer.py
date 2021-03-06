#This script makes the QCM_PICKUP node in \\magnetics::top.active_mhd:signals:qcm_pickup point to \\magnetics::top.shoelace:v_pickup
#Ted Golfinopoulos
#23 Apr 2012

import sys #For getting command line arguments
from MDSplus import *

if(len(sys.argv)>1) :
	s1=int(sys.argv[1]) #Grab shot number from command line.
else :
	s1=-1 #Default to shot -1

if(len(sys.argv)>2) :
	s2=int(sys.argv[2]) #Grab shot number from command line.
else :
	s2=s1 #Only do a single shot.

for s in range(s1,s2+1) :
	tree=Tree('magnetics',s) #Get the tree.
	tree.getNode('active_mhd:signals:qcm_pickup').putData(Data.compile('\MAGNETICS::TOP.SHOELACE:V_PICKUP')) #Point QCM_PICKUP node to node in SHOELACE subtree, which is processed.
	print('ACTIVE_MHD:SIGNALS:QCM_PICKUP now points to SHOELACE:V_PICKUP for Shot {0:d}'.format(s))

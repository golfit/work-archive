#SetupCalibrationNodes.py
#This script puts calibration nodes into a tree to prepare for I/V box voltage calibration.
#Ted Golfinopoulos, 20 Feb 2012

import sys #For getting command line arguments
from MDSplus import *

if(len(sys.argv)>1) :
	s1=int(sys.argv[1]) #Grab shot number from command line.
else :
	s1=-1 #Default to shot -1

if(len(sys.argv)>2) :
	s2=int(sys.argv[2]) #Grab shot number from command line.
else :
	s=s2 #Default to shot -1

def addCalibNodes(tree,node,boxNum) :
	tree.setDefault(node)
	#Add box number node

    #Nodes to add into tree - tuple pairs/triplets are (node_name, node_type{,parent_node})
    nodesToAdd=[('box_num','signal'),('calibrated','signal'), ('cal_vs_freq','signal'),('H_real','numeric','cal_vs_freq'),('H_imag','numeric','cal_vs_freq'), ('freq_axis','numeric','cal_vs_freq')]
	
    #try each one - skip if failed - probably already there.
	for ii in range(0, len(nodesToAdd)) :
        try :
            if(len(nodesToAdd[ii])==3) : #Third argument in tuple is parent node, if it's there
                baseNode=tree.getNode(nodesToAdd[ii][2])
            else : #No subnode specified - place node in default layer
                baseNode=tree.getDefault()

	        baseNode.addNode(nodesToAdd[ii][0],nodesToAdd[ii][1]) #Add node to tree: addNode(node_name,node_type)
	    except :
	        print("Can't add node "+nodesToAdd[ii][0]+"- already exists")

	#Put box number into node
    tree.getNode('box_num').putData(boxNum)
    

for s in range(s1,s2+1) :
	tree=Tree('Magnetics',s,'edit')

	#antVNode=tree.getNode('\\magnetics::top.shoelace:ant_v')
	#srcVNode=tree.getNode('\\magnetics::top.shoelace:src_v')
	#pickupNode=tree.getNode('\\magnetics::top.shoelace:v_pickup')
	#spareVNode=tree.getNode('\\magnetics::top.shoelace:spare_v')
	src2VNode=tree.getNode('\\magnetics::top.shoelace:src2_v')

	#addCalibNodes(tree,antVNode,2)
	#addCalibNodes(tree,srcVNode,3)
	#addCalibNodes(tree,pickupNode,4)
	addCalibNodes(tree,src2VNode,1)

	#Write changes to tree
	tree.write()

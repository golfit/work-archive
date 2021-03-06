#SetupSource2Nodes.py
#This script puts a node for the spare I/V box in the Shoelace subtree for characterizing input from the second T&C AG1010 (belonging to JET via Paul Woskov) amplifier.  It has appropriate calibration nodes.
#Ted Golfinopoulos, 30 May 2012

import sys #For getting command line arguments
from MDSplus import *

if(len(sys.argv)>1) :
	s=int(sys.argv[1]) #Grab shot number from command line.
else :
	s=-1 #Default to shot -1

tree=Tree('Magnetics',s,'edit')

tree.setDefault(tree.getNode('shoelace')) #Set default to top level of shoelace subtree.
tree.addNode('src_v_2', 'signal')
tree.addNode('src_i_2', 'signal')

voltageNode=tree.getNode('\\magnetics::top.shoelace:src_v_2')
currentNode=tree.getNode('\\magnetics::top.shoelace:src_i_2')

def setupNode(tree,node,boxNum, comment, cal) :
	node.putData(Data.compile(node.getPath()+':raw * '+node.getPath()+':cal'))
	tree.setDefault(node)
	tree.addNode('comment','text')
	tree.addNode('raw','signal')
	tree.addNode('cal','numeric')
	tree.getNode('cal').putData(cal)
	#Add box number node
	tree.addNode('box_num','numeric')
	tree.getNode('box_num').putData(boxNum)
	#Add calibrated node
	tree.addNode('calibrated','signal')
	tree.getNode('comment').putData('This node holds the '+comment+' data for the second amplifier (using an additional current/voltage probe box).')

setupNode(tree,voltageNode,1,'voltage',200.9)
setupNode(tree,currentNode,1,'current',100.0)

#Write changes to tree
tree.write()

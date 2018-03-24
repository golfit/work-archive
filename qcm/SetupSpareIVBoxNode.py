#SetupSpareIVBoxNode.py
#This script puts a node for the spare I/V box in the Shoelace subtree with appropriate calibration nodes.
#Ted Golfinopoulos, 15 Mar 2012

import sys #For getting command line arguments
from MDSplus import *

if(len(sys.argv)>1) :
	s=int(sys.argv[1]) #Grab shot number from command line.
else :
	s=-1 #Default to shot -1

tree=Tree('Magnetics',s,'edit')

tree.setDefault(tree.getNode('shoelace')) #Set default to top level of shoelace subtree.
tree.addNode('spare_v', 'signal')
tree.addNode('spare_i', 'signal')

voltageNode=tree.getNode('\\magnetics::top.shoelace:spare_v')
currentNode=tree.getNode('\\magnetics::top.shoelace:spare_i')

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
	tree.getNode('comment').putData('This is a convenience node to hold data for the '+comment+' from the spare current/voltage probe box.  Its use will vary.  A description should be put here.')

setupNode(tree,voltageNode,1,'voltage',200.9)
setupNode(tree,currentNode,1,'current',100.0)

#Write changes to tree
tree.write()

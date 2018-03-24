'''
This script runs through a range of shots and toggles the state of the data nodes associated with antenna and source voltage and current.
'''

import sys
from MDSplus import *

s1=int(sys.argv[1])

#Get shot range
if(len(sys.argv)>2) :
	s2=int(sys.argv[2])
else :
	s2=s1

def toggleNode(n) :
	n.setOn(not n.isOn())

for s in range(s1,s2+1) :
	tree=Tree('magnetics',s) #Get tree out of MDSplus
	toggleNode(tree.getNode('shoelace:ant_v'))
	toggleNode(tree.getNode('shoelace:ant_i'))
	toggleNode(tree.getNode('shoelace:src_v'))
	toggleNode(tree.getNode('shoelace:ant_i'))
	print("Toggled Shoelace power nodes for shot {0:d}".format(s))


#This function adds a Hilbert transform node to the antenna current in the magnetics tree.
#Ted Golfinopoulos, 7 June 2012
from MDSplus import *
import re
import sys #For getting command line arguments

#Parse command line arguments.
if(len(sys.argv)>1) :
	s1=int(sys.argv[1]) #Grab shot number from command line.
else :
	s1=-1 #Default to shot -1

if(len(sys.argv)>2) :
	s2=int(sys.argv[2]) #Grab shot number from command line.
elif(s1==-1) :
	s2=s1 #If s1 is the model tree, only do s=-1; don't run to s=0
else :
	s2=s1 #Only do a single shot

for s in range(s1,s2+1) :
	tree=Tree('magnetics',s,'edit') #Open tree to add node.
	tree.getNode('shoelace.ant_i').addNode('hilb','signal')
	tree.write() #Write change to tree
	print('Added shoelace.ant_i.hilb signal node, shot={0:d}'.format(s))

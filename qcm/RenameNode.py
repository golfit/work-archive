#This script reads in a node name from-to replacement string pair from the command line and applies the changes to a specified node for a specified shot range.
#Ted Golfinopoulos, 31 May 2012
from MDSplus import *
import re
import sys #For getting command line arguments

#Parse command line arguments.
if(len(sys.argv)>3) :
	s1=int(sys.argv[3]) #Grab shot number from command line.
else :
	s1=-1 #Default to shot -1

if(len(sys.argv)>4) :
	s2=int(sys.argv[4]) #Grab shot number from command line.
elif(s1==-1) :
	s2=s1 #If s1 is the model tree, only do s=-1; don't run to s=0
else :
	s2=s1 #Only do a single shot

if(len(sys.argv)>5) :
	treeName=sys.argv[5] #Name of tree
else :
	treeName='magnetics' #Default tree name
	print('Defaulting to magnetics tree.')

if(len(sys.argv)>1) :
	oldNodeName=sys.argv[1]
else :
	print("Must enter a valid node name in magnetics tree")
	s1=0
	s2=-1

if(len(sys.argv)>2) :
	newNodeName=sys.argv[2]
else :
	print("Must enter new node name")
	s1=0
	s2=-1

#Loop through range of shots
for s in range(s1,s2+1) :
	tree=Tree(treeName,s,'edit')
	n=tree.getNode(oldNodeName)

	try :
		n.rename(newNodeName)
		print(('Shot {0:d} - renamed node from '+oldNodeName+' to '+newNodeName).format(s))
		tree.write() #Write changes to tree.
	except TreeNoDataException :
		#Continue
		print("Could rename "+n.getPath()+" for shot{0:d}; moving on.".format(s))





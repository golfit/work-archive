"""
This script creates a deep copy of an MDS tree 
"""

from MDSplus import *
import myTools
import sys

if(len(sys.argv)>1) :
	#Parse shot information, contained in first command-line argument
	sInputList=myTools.parseList(sys.argv[1])
else :
	sInputList=[-1]

if(len(sys.argv)>2) :
	#Parse shot output information, contained in first command-line argument
	sOutputList=myTools.parseList(sys.argv[2])
else :
	sOutputList=[1120903900]

if(len(sInputList) != len(sOutputList)) :
	raise IOError('Input and output shot lists have same length.')

stringArgs=sys.argv[3:]
#List of nodes in remaining command line arguments

stringArgs=sys.argv[2:]

s=1120831700
sOut=1120831701

tree=Tree('magnetics',s)
outTree=Tree('magnetics',sOut)

allNodes=tree.getNodeWild('***')

#for n in allNodes :
#	print(n.getFullPath())

for n in allNodes :
	print('Processing '+n.getFullPath())
	outTree.getNode(n.getFullPath()).putData(n.getData());
	print('Got data from s=(0:d)'.format(s)+', '+n.getFullPath()+' and put it in s=(0:d)'.format(sOut)+', '+outTree.getNode(n.getFullPath()))

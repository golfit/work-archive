#This script reads in one or a list of shot numbers (ranges specified by colon), as well as one or more node names, and turns off the nodes in the tree for the specified shots.
#Ted Golfinopoulos, 14 Aug 2012

from MDSplus import *
import sys #For getting command line arguments
import myTools
import re

#Parse shot information, contained in first command-line argument
sList=myTools.parseList(sys.argv[1])

#List of nodes in remaining command line arguments

stringArgs=sys.argv[2:]

for s in sList :

	nodeList=stringArgs #Otherwise, user has specified list of signals, explicitly.

	for nodeName in nodeList :
		#Parse tree name
		extractTreeName=re.findall('(\\\)(.+)(::)',nodeName)
		if(len(extractTreeName)==0) :
			treeName='magnetics'
		else :
			treeName = extractTreeName[0][1] #Second argument from regular expression output is tree name

		print("Shot={0:d}".format(s)+" and tree="+treeName+" and node="+nodeName)

		extractProbeName=re.split('(:)|(\\.)',nodeName)
		probeName=extractProbeName[-1] #Last argument in nodeName broken at node dividers is probe name.

		nodeName="\\"+nodeName

		tree=Tree(treeName,s)
		n=tree.getNode(nodeName)

		try :
			n.setOn(False) #Turn node off.
			#print('I would turn off: '+n.getPath())
		except TreeNoDataException :
			print('No data in node '+n.getPath()+'; moving on.')

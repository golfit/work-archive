#This script processes the calculation of the maximum in the center frequency of a signal
#Ted Golfinopoulos, 13 June 2012

from MDSplus import *
import sys #For getting command line arguments
import numpy
import myTools
from scipy.fftpack import hilbert
from scipy.interpolate import interp1d
import re
from calcTransFun import *
from calcCenterFreq import *
from myTools import smooth, myDownsampleWithSmooth, getYX
from sigProc import cohere #Credit to John D. Hunter for this library
import pdb

#Parse shot information, contained in first command-line argument
sList=myTools.parseList(sys.argv[1])

#List of nodes in remaining command line arguments

stringArgs=sys.argv[2:]

#Loop through shots in list
for s in sList :
	print("Shot {0:d}".format(s))

	#Open magnetics tree to get Shoelace antenna signal.
	magTree=Tree('magnetics',s, 'edit')

	#By default, cross-correlation flag is false.
	crossCorrFlag=False

	if(s<1110000000) : antNode=magTree.getNode('active_mhd.signals:i_gh_upper_z') #Old current node for Active MHD antenna - for comparison with Jason Sears' work.
	else : antNode=magTree.getNode('shoelace.ant_i') #Shoelace antenna current node.

	#Check to see if antenna current node is on - if it is not, skip and continue.
	if(not(antNode.isOn())):
		print("Antenna current node is off for Shot {0:d} - don't process any cross-correlation".format(s))
		crossCorrFlag=False

	usePremadeListFlag=False #Flag to indicate whether user has specified a premade list of nodes, or has entered them explicitly at the command line.
	nodeList=[] #Initialize variable to hold paths of list of "output signal" nodes - calculate transfer function for these signals.

	nodeList,ceceNodes=myTools.parsePremadeNodeList(stringArgs, s)

	if(len(nodeList)>0) : usePremadeListFlag=True

	if(not(usePremadeListFlag)) :
		nodeList=stringArgs #Otherwise, user has specified list of signals, explicitly.

	#Loop through nodes for which transfer function is desired
	for nodeName in nodeList :
		if( hasattr(nodeName, '__iter__') ) :
			nodeSubList=nodeName
			nodeName=nodeName[0] #For now, just use first element in sublist of nodes for getting tree, name, etc.
		else :
			nodeSubList=[nodeName]

		#Parse tree name
		extractTreeName=re.findall('(\\\)(.+)(::)',nodeName)
		if(len(extractTreeName)==0) :
			sigTree=magTree #Default tree is magnetics
			treeName='magnetics'
		else :
			treeName = extractTreeName[0][1] #Second argument from regular expression output is tree name
			sigTree=Tree(treeName,s)

		extractProbeName=re.split('(:)|(\\.)',nodeName)
		probeName=extractProbeName[-1] #Last argument in nodeName broken at node dividers is probe name.

		#Add up and down to names of ASP probes.
		if( re.search('.UP:',nodeName) ) : probeName=probeName+"UP"
		elif( re.search('.DN:',nodeName ) ) : probeName=probeName+"DN"

		#Handle situation when there are multiple nodes for this element in nodeList.
		#If there are two nodes, this implies an I and Q quadrature pair.  Treat as real and imaginary parts.
		#If more than two, find some of squares.
		#If just one node, grab the data from this node.
		y=numpy.array([0.0]) #Initialize array.
		scaleFac=1.0
		for myNode in nodeSubList :
			print(myNode)
			sigNode=sigTree.getNode(myNode)
		        #See if node is on; if it is off, skip and go to next.
			if( not(sigNode.isOn()) ) :
				print("Node, "+str(sigNode.getPath())+" is off; skipping and continuing")
				skipNode=True
				break
			else :
				skipNode=False

		if(skipNode) :
			continue

		if(s<1110000000) : topNode=magTree.getNode('active_mhd')
		else : topNode=magTree.getNode('shoelace')

		try :
			#Add new tree node to hold transfer functions
			topNode.addNode('peak_freq','structure')

			#Write changes to tree.
			magTree.write()
		except :
			print("...can't add peak_freq structure node - may exist already")

		peakFreqNode=topNode.getNode('peak_freq')

		try :
			#Add a node for each coil
			peakFreqNode.addNode(probeName,'signal')

			#Add sub-nodes for node.
			n=peakFreqNode.getNode(probeName)
			
			n.addNode('raw','signal')
			if( crossCorrFlag ) :
				n.addNode('Hr','signal')
				n.addNode('Hi','signal')
				n.addNode('H','signal')
				n.addNode('Cxy','signal') #Cross coherence
			n.addNode('comment','text')

			#Write changes to tree.
			magTree.write()
		except :
			n=peakFreqNode.getNode(probeName)
			print("...peak frequency subnodes for "+probeName+" are already there")

		print("Made nodes in "+n.getPath()+" for Shot {0:d}".format(s))
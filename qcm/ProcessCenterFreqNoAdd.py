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
	magTree=Tree('magnetics',s)

	if(s>1110500000) :
		fRange=numpy.array([40.0,250.0])*1.0E3
	else :
		fRange=numpy.array([40.0,1250.0])*1.0E3

	#By default, cross-correlation flag is false.
	crossCorrFlag=False

	#Get amplifier on and off times
	try :
		t1=magTree.getNode('shoelace.rf_gate.on').getData().evaluate().data()
		t2=magTree.getNode('shoelace.rf_gate.off').getData().evaluate().data()
	except :
		t1=0.5
		t2=1.5
		print('Gate times set at 0.5 and 1.5 s')

	if(s<1110000000) : antNode=magTree.getNode('active_mhd.signals:i_gh_upper_z') #Old current node for Active MHD antenna - for comparison with Jason Sears' work.
	else : antNode=magTree.getNode('shoelace.ant_i') #Shoelace antenna current node.

	#Check to see if antenna current node is on - if it is not, skip and continue.
	if(not(antNode.isOn())):
		print("Antenna current node is off for Shot {0:d} - don't process any cross-correlation".format(s))
		crossCorrFlag=False
	elif(t2-t1<=0.001) : #Check to make sure antenna actually ran - this is not a perfect check, but is one way to avoid wasted computation during the shot cycle.
		print("Antenna is gated off for Shot {0:d} - don't process cross-correlation for this shot, but try to get center frequency.".format(s))
		crossCorrFlag=False
	else :
		#Get timebase and signal.
		ti=antNode.getData().evaluate().dim_of().data() #Timebase of current signal
		fs=1./(ti[1]-ti[0]) #Sampling frequency.

		ia=antNode.getData().evaluate().data() #Antenna current signal [A]

		#Get antenna current amplitude - downsample.
		iamp=numpy.sqrt(2.0*myDownsampleWithSmooth(pow(ia[numpy.logical_and(ti>t1,ti<t2)],2),100))
		tiamp=numpy.linspace(t1,t2,len(iamp)) #Make timebase for iamp
		fsIamp=1.0/(tiamp[1]-tiamp[0])

		iampHilb=iamp-1j*hilbert(iamp)

	usePremadeListFlag=False #Flag to indicate whether user has specified a premade list of nodes, or has entered them explicitly at the command line.
	nodeList=[] #Initialize variable to hold paths of list of "output signal" nodes - calculate transfer function for these signals.

	nodeList,ceceNodes=myTools.parsePremadeNodeList(stringArgs, s)

	if(len(nodeList)>0) : usePremadeListFlag=True

	#Calculate cross-correlation component if requested.
#	if( any([x=="crosscorr" for x in stringArgs]) or any([x=="mscohere" for x in stringArgs]) ) : crossCorrFlag=True
#	else : crossCorrFlag=False

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

                        #Get signal of node.
			if(len(nodeSubList)==1) :
				y,t=getYX(sigNode)
			elif(len(nodeSubList)==2) :
				yTemp,t=getYX(sigNode)#"Output" signal
				y=y+scaleFac*yTemp
				scaleFac=scaleFac*1j
			else :
				yTemp,t=getYX(sigNode)#"Output" signal
				y=y+pow(yTemp,2)

		if(skipNode) :
			continue

		if(len(nodeSubList)>2) : y = sqrt(y)

		if(max(abs(y))==0.E0) : #If signal is dead - skip the node and move to next.
			print("Signal from "+sigNode.getPath()+"is zeroed out - skipping and moving on.")
			continue

		#Get min and max times again, as available from signal.
		t1=max(t1,t[0])
		t2=min(t2,t[-1])

		fsSig=1.0/(t[1]-t[0])

		#Get peak frequency in y.
		fp,tp = getFPeak( y, fsSig, fRange, 1024 ) #Use nfft=1024 since this worked well at workstation.
		tp=tp+t[0] #Shift time axis of frequency peaks according to start time of signal.

		 #Get cross coherence between antenna amplitude and peak freq.
		if( crossCorrFlag ) :
		#Calculate transfer function
			tpSub=tp[logicAnd(tp>=t1,tp<=t2)]
			interpObj=interp1d(tpSub,fp[logicAnd(tp>=t1,tp<=t2)])
			tpUp=tiamp[logicAnd(logicAnd(logicAnd(tiamp>t1,tiamp<t2),tiamp>tpSub[0]),tiamp<tpSub[-1])]
			fpUp=interpObj(tpUp)

			#Upsample peak frequency to antenna current amplitude timebase.
			H=calcTransFun(fpUp,iampHilb[logicAnd(tiamp>t1,tiamp<t2)],[75.E0,1.E4],fsIamp,50.E0) #Let transfer function be band-limited with upper-bound 10% of lower bound of frequency range of interest.

			tH=linspace(t1,t2,len(H)) #Make a new timebase corresponding to transfer function.

			nfft=8*int(pow(2,numpy.ceil(numpy.log2(numpy.sqrt(2.0*len(tiamp))))))
			Cxy,fCxy=cohere(iamp[logicAnd(tiamp>1.0,tiamp<1.5)],fpUp[logicAnd(tpUp>1.0,tpUp<1.5)],nfft,fsIamp,noverlap=int(numpy.floor(nfft/16)))
			#Re-cast to Numpy types.
			Cxy=numpy.array(Cxy)
			fCxy=numpy.array(fCxy)

		if(s<1110000000) : topNode=magTree.getNode('active_mhd')
		else : topNode=magTree.getNode('shoelace')

		peakFreqNode=topNode.getNode('peak_freq')

		n=peakFreqNode.getNode(probeName)

		#Add a comment describing nodes.
		n.getNode('comment').putData('parent node=frequency [Hz] at which max in power spectrum occurs in band, {0:f}<f<{1:f} (independent variable=time in s); H=transfer function [Hz/A] between antenna current and peak frequency  (independent variable=time in s); Hr and Hi are real and imaginary parts of H; Cxy=cross coherence between antenna current amplitude and peak frequency (independent variable=frequency in Hz); raw points to data used to extract peak frequency'.format(fRange[0],fRange[1]))

		#Prepare expression to put in tree with data.
		n.putData(Data.compile("BUILD_SIGNAL($VALUE,$1,$2)",fp,tp)) #Put center frequency data in tree.

		n.getNode('raw').putData(Data.compile(nodeName)) #Put pointer to raw data of signal.

		if( crossCorrFlag ) : 
			#Put transfer function in tree as array of complex numbers.
			expr=Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", H, tH)
			n.getNode('H').putData(expr)

			#Make nodes that get real and imaginary parts of transfer function for implementations of MDS interface which can't handle getting complex types.
			n.getNode('Hr').putData(Data.compile("real(H)"))
			n.getNode('Hi').putData(Data.compile("aimag(H)"))
			n.getNode('Cxy').putData(Data.compile("BUILD_SIGNAL($VALUE,$1,$2)",Cxy,fCxy))

		print("Put data in "+n.getPath()+" for Shot {0:d}".format(s))

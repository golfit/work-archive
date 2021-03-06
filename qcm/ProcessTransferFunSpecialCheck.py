#This script uses the same processing for the transfer function as normal, but does so for a particular situation: take the fluctuation data from one shot in which the Shoelace antenna didn't run, and the current data from a shot in which the Shoelace was operating, and calculate the transfer function.  This way, we can perform a check on whether there are false positives in the scheme for picking up poles.
#Ted Golfinopoulos, 13 June 2012

from MDSplus import *
import sys #For getting command line arguments
import numpy
import myTools
from scipy.fftpack import hilbert
from scipy.interpolate import interp1d
import re
from calcTransFun import *


#Parse shot information, contained in first command-line argument
sList=[1120815018]#1120712021] #A shot for which there was a QCM, but the Shoelace wasn't operating.
sShoelace=1120814021#1120712023 #A shot for which the Shoelace was running.
sOut=1120814800 #Put data here.

#List of nodes in remaining command line arguments

stringArgs=sys.argv[1:]

def getDataInRange(srcNode,t1,t2) :
	myStr="_y="+n.getPath()+", _t=dim_of("+n.getPath()+"), pack(_y, _t > {0:f} and _t < {0:f})".format(t1,t2)
	t1Actual=Data.compile("_t=dim_of("+n.getPath()+ "), _t[firstloc(_t > {0:f} and _t < {0:f})]".format(t1,t2) ).evaluate().data()
	t2Actual=Data.compile("_t=dim_of("+n.getPath()+ "), _t[lastloc(_t > {0:f} and _t < {0:f})]".format(t1,t2) ).evaluate().data()
	y=Data.compile( myStr ).evaluate().data() #Grab data in specified range
	return y, linspace(t1Actual,t2Actual,len(y)) #Regenerate timebase locally


#Loop through shots in list
for s in sList :
	#Open magnetics tree to get Shoelace antenna signal.
	magTree=Tree('magnetics',s)
	shoeTree=Tree('magnetics',sShoelace)
	outTree=Tree('magnetics',sOut,'edit')

	#Get frequency points to extract range of frequencies.
	fpts=shoeTree.getNode('shoelace.freq_program.freq_wave_hz').getData().evaluate().data() #For Shoelace antenna work

	freqPad=5.E3 #Extend frequency range by this amount - padding.
	fRange=numpy.array([min(fpts)-freqPad,max(fpts)+freqPad])

	#Get amplifier on and off times
	try :
		t1=shoeTree.getNode('shoelace.rf_gate.on').getData().evaluate().data()
		t2=shoeTree.getNode('shoelace.rf_gate.off').getData().evaluate().data()
	except :
		t1=0.5
		t2=1.5
		print('Gate times set at 0.5 and 1.5 s')

	antNode=shoeTree.getNode('shoelace.ant_i') #Shoelace antenna current node.

	#Check to see if antenna current node is on - if it is not, skip and continue.
	if(not(antNode.isOn())):
		print("Antenna current node is off for Shot {0:d} - skip and continue".format(s))
		continue
	elif(t2-t1<=0.001) : #Check to make sure antenna actually ran - this is not a perfect check, but is one way to avoid wasted computation during the shot cycle.
		print("Antenna is gated off for Shot {0:d} - skip and continue".format(s))
		continue

	#Get timebase and signal.
	ti=antNode.getData().evaluate().dim_of().data() #Timebase of current signal
	fs=1./(ti[1]-ti[0]) #Sampling frequency.

	ia=antNode.getData().evaluate().data() #Antenna current signal [A]

	try :
		iaHilb=ia+1j*antNode.getNode('hilb').getData().evaluate().data() #Hilbert transform of current signal
	except : #If there's no hilbert transform node, calculate it.
		iaHilb=ia-1j*hilbert(ia)
		expr=Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", numpy.imag(iaHilb), ti)
		antNode.getNode('hilb').putData(expr)

	usePremadeListFlag=False #Flag to indicate whether user has specified a premade list of nodes, or has entered them explicitly at the command line.
	nodeList=[] #Initialize variable to hold paths of list of "output signal" nodes - calculate transfer function for these signals.

	nodeList,ceceNodes=myTools.parsePremadeNodeList(stringArgs, s)

	if(len(nodeList)>0) : usePremadeListFlag=True

	#Calculate cross-correlation component if requested.
	if( any([x=="crosscorr" for x in stringArgs]) or any([x=="mscohere" for x in stringArgs]) ) : crossCorrFlag=True
	else : crossCorrFlag=False

	if(not(usePremadeListFlag)) :
		nodeList=stringArgs #Otherwise, user has specified list of signals, explicitly.

	#Loop through nodes for which transfer function is desired
	for nodeName in nodeList :
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

		print('test')
		print(nodeName)
		sigNode=sigTree.getNode(nodeName)
		#See if node is on; if it is off, skip and go to next.
		if( not(sigNode.isOn()) ) :
			print("Node, "+str(sigNode.getPath())+" is off; skipping and continuing")
			continue

		#Get signal of node.
		y=sigNode.getData().evaluate().data() #"Output" signal - calculate transfer function with respect to this.

		#If signal is not from magnetics tree, resample onto magnetics timebase.
		if(treeName.lower()!='magnetics') :
			tsig=sigTree.getNode(nodeName).getData().evaluate().dim_of().data() #Signal timebase
			t1,t2=[max(t1,tsig[0]),min(t2,tsig[-1])] #Might need to change data range if signal time base does not extend to full pulse of input signal.
			interpObj=interp1d(tsig,y)
			y=interpObj(ti[numpy.logical_and(ti>t1,ti<t2)]) #Interpolate y only in time range of interest.
		else : #Otherwise, just reduce size of y to time range of interest.
			y = y[numpy.logical_and(ti>t1,ti<t2)]

		#Calculate transfer function
		H=calcTransFun(y,iaHilb[numpy.logical_and(ti>t1,ti<t2)],fRange,fs)
		if( crossCorrFlag == True ) :
			Hyx=calcTransFun(ia[numpy.logical_and(ti>t1,ti<t2)],y-1j*hilbert(y),fRange,fs)
			Cxy=H*Hyx #Cross-coherence spectrum for component.  This follows since Hxy=Pxy/Pxx, and Hyx=Pyx/Pyy=Pxy'/Pyy, and Cxy:=|Pxy|^2/(Pxx*Pyy), where the prime denotes complex conjugation.

		tH=linspace(t1,t2,len(H)) #Make a new timebase corresponding to transfer function.

		topNode=outTree.getNode('shoelace')

		try :
			#Add new tree node to hold transfer functions
			topNode.addNode('trans_fun','structure')

			#Write changes to tree.
			outTree.write()
		except :
			print("...can't add trans_fun structure node - may exist already")

		transFunNode=topNode.getNode('trans_fun')

		try :
			#Add a node for each coil
			transFunNode.addNode(probeName,'signal')

			#Add sub-nodes for node.
			n=transFunNode.getNode(probeName)
			
			n.addNode('raw','signal')
			n.addNode('Hr','signal')
			n.addNode('Hi','signal')

			#Write changes to tree.
			outTree.write()
		except :
			n=transFunNode.getNode(probeName)
			print("...transfer function subnodes for "+probeName+" are already there")

		#Prepare expression to put in tree with data.
		#Put transfer function in tree as array of complex numbers.
		expr=Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", H, tH)
		n.putData(expr)

		n.getNode('raw').putData(Data.compile(nodeName)) #Put pointer to raw data of signal.

		#Make nodes that get real and imaginary parts of transfer function for implementations of MDS interface which can't handle getting complex types.
		n.getNode('Hr').putData(Data.compile("real("+n.getPath()+")"))
		n.getNode('Hi').putData(Data.compile("aimag("+n.getPath()+")"))
	
		print("Put transfer function data in "+n.getPath())
		#######################Cross-coherence
		if(crossCorrFlag) :
			try :
				#Add new tree node to hold cross-coherence
				topNode.addNode('mscohere','structure')

				#Write changes to tree.
				outTree.write()
			except :
				print("...can't add mscohere structure node - may exist already")

			mscohereNode=topNode.getNode('mscohere')

			try :
				#Add a node for each coil
				mscohereNode.addNode(probeName,'signal')

				#Add sub-nodes for node.
				n=mscohereNode.getNode(probeName)
			
				n.addNode('raw','signal')

				#Write changes to tree.
				outTree.write()
			except :
				n=mscohereNode.getNode(probeName)
				print("...magnitude squared coherence subnodes for "+probeName+" are already there")

			#Prepare expression to put in tree with data.
			#Put transfer function in tree as array of complex numbers.
			expr=Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", Cxy, tH)
			n.putData(expr)

			n.getNode('raw').putData(Data.compile(nodeName)) #Put pointer to raw data of signal.

			print("Put magnitude square coherence component data in "+n.getPath())

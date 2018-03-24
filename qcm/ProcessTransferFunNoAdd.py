#This script processes the transfer function between the Shoelace antenna current and pickup signals (e.g. Mirnov coils, etc.)
#Ted Golfinopoulos, 13 June 2012

from MDSplus import *
import sys #For getting command line arguments
import numpy
import myTools_no_sql as myTools
from scipy.fftpack import hilbert
from scipy.interpolate import interp1d
import re
from calcTransFun import *


#Parse shot information, contained in first command-line argument
sList=myTools.parseList(sys.argv[1])

#List of nodes in remaining command line arguments

stringArgs=sys.argv[2:]

def getDataInRange(srcNode,t1,t2) :
	myStr="_y="+n.getPath()+", _t=dim_of("+n.getPath()+"), pack(_y, _t > {0:f} and _t < {0:f})".format(t1,t2)
	t1Actual=Data.compile("_t=dim_of("+n.getPath()+ "), _t[firstloc(_t > {0:f} and _t < {0:f})]".format(t1,t2) ).evaluate().data()
	t2Actual=Data.compile("_t=dim_of("+n.getPath()+ "), _t[lastloc(_t > {0:f} and _t < {0:f})]".format(t1,t2) ).evaluate().data()
	y=Data.compile( myStr ).evaluate().data() #Grab data in specified range
	return y, linspace(t1Actual,t2Actual,len(y)) #Regenerate timebase locally


#Loop through shots in list
for s in sList :
	print("Shot {0:d}".format(s))

	#Open magnetics tree to get Shoelace antenna signal.
	magTree=Tree('magnetics',s)

	#Get frequency points to extract range of frequencies.
	if(s < 1110000000 ) : #For Active MHD shots
		ftae,tftae=myTools.getYX(magTree.getNode('\MAGNETICS::TOP.ACTIVE_MHD.DPCS:FTAE_CALC'))
		deltaf=magTree.getNode('\MAGNETICS::TOP.ACTIVE_MHD.DPCS:DELTAF').getData().evaluate().data()
		tftae=numpy.linspace(tftae[0],tftae[-1],len(ftae))
		ftae=ftae[numpy.logical_and(tftae>0.5,tftae<1.5)]
		fpts=[min(ftae)-deltaf,max(ftae)+deltaf]
#	else : fpts=magTree.getNode('shoelace.freq_program.freq_wave_hz').getData().evaluate().data() #For Shoelace antenna work
	else : fpts=magTree.getNode('shoelace.freq_program.vco_freq').getData().evaluate().data() #For Shoelace antenna work
	freqPad=5.E3 #Extend frequency range by this amount - padding.
	fRange=numpy.array([min(fpts)-freqPad,max(fpts)+freqPad])

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
		H=calcTransFun(y,iaHilb[numpy.logical_and(ti>t1,ti<t2)],fRange,fs,min(fRange)*0.1) #Let transfer function be band-limited with upper-bound 10% of lower bound of frequency range of interest.
		if( crossCorrFlag == True ) :
			Hyx=calcTransFun(ia[numpy.logical_and(ti>t1,ti<t2)],y-1j*hilbert(y),fRange,fs,min(fRange)*0.1)
			Cxy=H*Hyx #Cross-coherence spectrum for component.  This follows since Hxy=Pxy/Pxx, and Hyx=Pyx/Pyy=Pxy'/Pyy, and Cxy:=|Pxy|^2/(Pxx*Pyy), where the prime denotes complex conjugation.

		tH=linspace(t1,t2,len(H)) #Make a new timebase corresponding to transfer function.

		if(s<1110000000) : topNode=magTree.getNode('active_mhd')
		else : topNode=magTree.getNode('shoelace')

		transFunNode=topNode.getNode('trans_fun')

		try :
			#Add sub-nodes for node.
			n=transFunNode.getNode(probeName)
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
	
		print("Put transfer function data in "+n.getPath()+" for Shot {0:d}".format(s))

		#######################Cross-coherence
		if( crossCorrFlag ) :
			mscohereNode=topNode.getNode('mscohere')

			try :
				#Add sub-nodes for node.
				n=mscohereNode.getNode(probeName)
			except :
				n=mscohereNode.getNode(probeName)
				print("...magnitude squared coherence subnodes for "+probeName+" are already there")

			#Prepare expression to put in tree with data.
			#Put transfer function in tree as array of complex numbers.
			expr=Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", Cxy, tH)
			n.putData(expr)

			n.getNode('raw').putData(Data.compile(nodeName)) #Put pointer to raw data of signal.

			print("Put magnitude square coherence component data in "+n.getPath()+" for Shot {0:d}".format(s))

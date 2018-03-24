#This script reads in a shot list and processes the cross coherence spectrogram between the given nodes and the antenna current signal.
#Ted Golfinopoulos, 16 Aug 2012

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

#Loop through shots in list
for s in sList :
	print("Shot {0:d}".format(s))

	#Open magnetics tree to get Shoelace antenna signal.
	magTreeOut=Tree('magnetics',sOut, 'edit') #Write data into this tree.
	magTreeIn=Tree('magnetics',sShoelace) #Read data from this tree.

	#Get frequency points to extract range of frequencies.
	if(s < 1110000000 ) : #For Active MHD shots
		ftae,tftae=myTools.getYX(magTreeIn.getNode('\MAGNETICS::TOP.ACTIVE_MHD.DPCS:FTAE_CALC'))
		deltaf=magTreeIn.getNode('\MAGNETICS::TOP.ACTIVE_MHD.DPCS:DELTAF').getData().evaluate().data()
		tftae=numpy.linspace(tftae[0],tftae[-1],len(ftae))
		ftae=ftae[numpy.logical_and(tftae>0.5,tftae<1.5)]
		fpts=[min(ftae)-deltaf,max(ftae)+deltaf]
	else : fpts=magTreeIn.getNode('shoelace.freq_program.freq_wave_hz').getData().evaluate().data() #For Shoelace antenna work
	freqPad=5.E3 #Extend frequency range by this amount - padding.
	fRange=numpy.array([min(fpts)-freqPad,max(fpts)+freqPad])

	#Get amplifier on and off times
	try :
		t1=magTreeIn.getNode('shoelace.rf_gate.on').getData().evaluate().data()
		t2=magTreeIn.getNode('shoelace.rf_gate.off').getData().evaluate().data()
	except :
		t1=0.5
		t2=1.5
		print('Gate times set at 0.5 and 1.5 s')

	if(s<1110000000) : antNode=magTreeIn.getNode('active_mhd.signals:i_gh_upper_z') #Old current node for Active MHD antenna - for comparison with Jason Sears' work.
	else : antNode=magTreeIn.getNode('shoelace.ant_i') #Shoelace antenna current node.

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

	usePremadeListFlag=False #Flag to indicate whether user has specified a premade list of nodes, or has entered them explicitly at the command line.
	nodeList=[] #Initialize variable to hold paths of list of "output signal" nodes - calculate transfer function for these signals.

	nodeList,ceceNodes=myTools.parsePremadeNodeList(stringArgs, s)

	if(len(nodeList)>0) : usePremadeListFlag=True

	if(not(usePremadeListFlag)) :
		nodeList=stringArgs #Otherwise, user has specified list of signals, explicitly.

	#Loop through nodes for which transfer function is desired
	for nodeName in nodeList :
		#Parse tree name
		extractTreeName=re.findall('(\\\)(.+)(::)',nodeName)
		if(len(extractTreeName)==0) :
			sigTree=magTreeIn #Default tree is magnetics
			treeName='magnetics'
		else :
			treeName = extractTreeName[0][1] #Second argument from regular expression output is tree name
			sigTree=Tree(treeName,s)

		sigNode=sigTree.getNode(nodeName)
		#See if node is on; if it is off, skip and go to next.
		if( not(sigNode.isOn()) ) :
			print("Node, "+str(sigNode.getPath())+" is off; skipping and continuing")
			continue

		probeName=sigNode.getNodeName() #Grab name of node.
#		extractProbeName=re.split('(:)|(\\.)',nodeName)
#		probeName=extractProbeName[-1] #Last argument in nodeName broken at node dividers is probe name.

		#Add up and down to names of ASP probes.
		if( re.search('.UP:',nodeName) ) : probeName=probeName+"UP"
		elif( re.search('.DN:',nodeName ) ) : probeName=probeName+"DN"

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

		#Calculate magnitude-squared cross-coherence spectrogram
		nfft=2048
		Cxy,f,t=myTools.cohereSpecgram(ia[numpy.logical_and(ti>t1,ti<t2)],y,nfft,fs)
		t=t-t[0]+ti[numpy.abs(ti-t1)==numpy.min(ti[ti>t1]-t1)] #Align timebases.

		if(s<1110000000) : topNode=magTreeOut.getNode('active_mhd')
		else : topNode=magTreeOut.getNode('shoelace')

		try :
			#Add new tree node to hold transfer functions
			topNode.addNode('cohere','structure')

			#Write changes to tree.
			magTreeOut.write()
		except :
			print("...can't add cohere structure node - may exist already")

		cohereNode=topNode.getNode('cohere')

		try :
			#Add a node for each coil
			cohereNode.addNode(probeName,'numeric')

			#Add sub-nodes for node.
			n=cohereNode.getNode(probeName)
			
			n.addNode('t_range','numeric')
			n.addNode('freq_range','numeric')
			n.addNode('n_time_pts','numeric')
			n.addNode('n_freq_pts','numeric')
			n.addNode('Cxy_r','numeric')
			n.addNode('Cxy_i','numeric')

			#Write changes to tree.
			magTreeOut.write()
		except :
			n=cohereNode.getNode(probeName)
			print("...coherence function subnodes for "+probeName+" are already there")

		#Prepare expression to put in tree with data.
		#Put transfer function in tree as array of complex numbers.
		expr=Data.compile("$1", Cxy)
		n.putData(expr)

		n.getNode('t_range').putData(Data.compile("[$1,$2]",t[0],t[-1])) #Put pointer to raw data of signal.
		n.getNode('freq_range').putData(Data.compile("[$1,$2]",f[0],f[-1])) #Put pointer to raw data of signal.
		n.getNode('n_time_pts').putData(Data.compile("$1",len(t))) #Put pointer to raw data of signal.
		n.getNode('n_freq_pts').putData(Data.compile("$1",len(f))) #Put pointer to raw data of signal.

		#Make nodes that get real and imaginary parts of transfer function for implementations of MDS interface which can't handle getting complex types.
		n.getNode('Cxy_r').putData(Data.compile("real("+n.getPath()+")"))
		n.getNode('Cxy_i').putData(Data.compile("aimag("+n.getPath()+")"))
	
		print("Put magnitude-squared cross coherence data in "+n.getPath()+" for Shot {0:d}".format(s))

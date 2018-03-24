"""
ProcessShoelaceMCB.py
This script manages interaction with the MDSplus tree for decoding output signals from the Master Controller Board (MCB).
It has dependencies on the MDSplus library, as well as the decodeSignal module (allowing the latter to avoid
dependencies on MDSplus).

It is run from the command line as

	python ProcessShoelaceMCB.py SHOT_NUMBER

	where shot number is the integer shot number to be processed.

It will throw an (unhandled) exception from MDSplus if there are any read errors.
#25 Jan 2012, Ted Golfinopoulos
"""
import sys
from MDSplus import *
from decodeSignal import *

s=int(sys.argv[1]) #0th argument is script name; first argument is shot number.  Parse integer.

def decoderMaster(nodeName,tree) :
	"""
	Side-effect method (i.e. no returns) which takes a node name for a node with the structure
	I'm using for encoded binary numbers, reads the data in the nodes/subnodes, and stamps the
	corresponding time series of encoded numbers into the given node.
	
	USAGE:
		decodeMaster(nodeName, tree)

	nodeName = name of node where time series will be put.  Must have sub-node called "RAW"
		in which raw waveform signal is stored, as well as subnode, "NBITS", with number
		of bits in encoded binary number

	tree = tree with default (directory) set to level which has node, nodeName, as a subnode.  Must have
		another numeric-type subnode called "ENCODER_CLK" containing the clock speed (in Hz) used by the encoder
		module - i.e. a divided down version of the clock frequency, e.g. 4.E6/16 [Hz].
	"""
	try :
		print("Processing "+nodeName+"...")
		node = tree.getNode(nodeName) #Node whose data we will process.

		#Check to see if node is on.  If off, don't process.
		if(node.isOn()) :
			#Grab raw waveform.
			rawNode=node.getNode("RAW")
			y=rawNode.getData().data() #Waveform [V], returned as a primitive data type.
			t=rawNode.getData().dim_of().data() #Time axis [s]
	
			#parse code
			#fclk=clock speed used by encoder - long calling sequence is because encoder clock rate
			#is a more global parameter; it is stored in the parent node that holds the individual signal
			#nodes (e.g. MCB_OUT, which
			#holds SER_CODE).
			fclk=node.getParent().getNode("ENCODER_CLK").getData().data()
			nbits=node.getNode("NBITS").getData().data() #Number of bits in binary number to be decoded

			tpts,nums=decodeSignal(y,t,fclk, nbits)

			#Build a TDI expression for storing signal 
			expr = Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", nums, tpts)
			node.putData(expr) #Stamp expression in node.
			print("Data put in "+nodeName+".")
		else :
			print(node.getPath()+' is off - skipping.')
	except :
		print("Couldn't process "+nodeName+" - skipping and continuing") #Print error message
		#print("Debugging!!!")
		#pdb.set_trace()
		#raise #Re-raise exception.


try :
	tree=Tree("MAGNETICS", s) #Open tree
	tree.setDefault(tree.getNode("\\MAGNETICS::TOP.SHOELACE.MCB_OUT"))

	#Process SER_CODE node, which is to contain the decoded binary numbers for the series capacitor bank logic state.
	nodeName="SER_CODE"
	decoderMaster(nodeName, tree)

	#Process PAR_CODE node, which is to contain the decoded binary numbers for the parallel capacitor bank logic state.
	nodeName="PAR_CODE"
	decoderMaster(nodeName, tree)

	#Process PAR_CODE node, which is to contain the decoded binary numbers for the parallel capacitor bank logic state.
	nodeName="N_PER"
	decoderMaster(nodeName, tree)

	#Process SER_DIAG node, which is to contain the decoded binary numbers for the series capacitor bank logic state, as read from the backplane using a diagnostics board.
	nodeName="SER_DIAG"
	decoderMaster(nodeName, tree)

	#Process PAR_DIAG node, which is to contain the decoded binary numbers for the parallel capacitor bank logic state, as read from the backplane using a diagnostics board.
	nodeName="PAR_DIAG"
	decoderMaster(nodeName, tree)
	
except :
	print("Error processing shot {0:d}".format(s))
	raise #Re-raise the exception.

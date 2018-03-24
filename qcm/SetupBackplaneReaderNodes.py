from MDSplus import *
from numpy import *
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

def nodeSetup(n) :
	n.addNode('comment','text')
	n.addNode('nbits','numeric')
	n.addNode('raw','signal')
	n.getNode('nbits').putData(7) #Seven bits in encoded data stream corresponding to series and parallel number.

for s in range(s1,s2+1):
	tree=Tree('magnetics',s,'edit') #Open tree for editing
	tree.setDefault(tree.getNode('shoelace.mcb_out'))
	tree.addNode('ser_diag','signal') #Add node for series code diagnostic which reads backplane number and outputs as an encoded stream
	tree.addNode('par_diag','signal') #Likewise for parallel capacitor code.

	nser=tree.getNode('ser_diag')
	nodeSetup(nser)
	nser.getNode('comment').putData('This node corresponds to output from a board which reads the series backplane signals and outputs an encoded data stream when the signal has been parsed.  nbits=# of bits in each message in data stream.  raw=data on digitizer.  Parent node=encoded back plane numbers at times where they are received.')
	nser.getNode('raw').putData(Data.compile('\magnetics::top.active_mhd.data_acq.cpci.acq_216_3.input_13'))


	npar=tree.getNode('par_diag')
	nodeSetup(npar)
	npar.getNode('comment').putData('This node corresponds to output from a board which reads the parallel backplane signals and outputs an encoded data stream when the signal has been parsed.  nbits=# of bits in each message in data stream.  raw=data on digitizer.  Parent node=encoded back plane numbers at times where they are received.')
	npar.getNode('raw').putData(Data.compile('\magnetics::top.active_mhd.data_acq.cpci.acq_216_3.input_14'))

	tree.write() #Write changes to tree.

from numpy import *
from MDSplus import *

execfile("SetUpMcbSubtree.py") #Run script to set up a test pulse.

#Now, put data in the pulse raw signal of SER_CODE
fpath="/home/golfit/data/ScopeData/C1SerialLogicTestN225to295kHzIn0pt5sGoesWithNclkTest.dat"
#Load data
dat=loadtxt(fpath)

#Not sure if the array class is causing problems.
t=dat[:,0]
y=dat[:,1]
#for i in range(0,len(dat[:,1])) :
#	t.append(dat[i,0])
#	y.append(dat[i,1])

#s is defined in SetUpMcbSubtree.py
tree=Tree("MAGNETICS", s)

tree.setDefault(tree.getNode("SHOELACE.MCB_OUT:SER_CODE"))

n=tree.getNode("RAW")

expr = Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", y, t) #Build a TDI expression for storing signal
n.putData(expr) #Stamp expression in node.



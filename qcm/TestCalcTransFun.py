from MDSplus import *
from numpy import *
from calcTransFun import *
from scipy.fftpack import *
from matplotlib import *
import pdb

#Grab test data from the tree.
#s=1120605025
#tree=Tree('magnetics',s,'edit')
#coilName="bp_bc_top"
##y=tree.getNode('active_mhd.signals.bp_ab_top').getData().evaluate().data()
##t=tree.getNode('active_mhd.signals.bp_ab_top').getData().evaluate().dim_of().data()
#y=tree.getNode('active_mhd.signals.'+coilName).getData().evaluate().data()
#t=tree.getNode('active_mhd.signals.'+coilName).getData().evaluate().dim_of().data()
#x=tree.getNode('shoelace.ant_i').getData().evaluate().data()
#xi=tree.getNode('shoelace.ant_i.hilb').getData().evaluate().data()

#Create test data.
fs=2.5E6 #Sampling frequency
t=linspace(0.,1.,fs+1)
f=97.321E3 #Test frequency
alpha=20.0*numpy.pi/180.0 #Phase difference by which y leads x.
y=3.21*cos(2*pi*f*t+alpha)
x=cos(2*pi*f*t)

print("Created test waveforms")

#Calculate Hilbert transform
xi=-hilbert(x)
print("Calculated Hilbert transform")

xHilb=x+1j*xi

fs=1./(t[1]-t[0])
fRange=numpy.array([20.,200.])*1000.

#t1=1.71
#t2=2.0
t1=0.5
t2=1.5

H=calcTransFun(y[logical_and(t>t1,t<t2)],xHilb[logical_and(t>t1,t<t2)],fRange,fs)
print("Calculated transfer function")
tH=linspace(t1,t2,len(H)) #Make a new timebase corresponding to transfer function.


#try :
#	#Add new tree node to hold transfer functions
#	tree.getNode('shoelace').addNode('trans_fun','structure')

#	#Add a node for each coil
#	tree.getNode('shoelace.trans_fun').addNode(coilName)

#	#Add sub-nodes for node.
#	n=tree.getNode('shoelace.trans_fun.'+coilName)
#	n.addNode('raw','signal')
#	n.addNode('Hr','signal')
#	n.addNode('Hi','signal')
#except :
#	n=tree.getNode('shoelace.structure.'+coilName)
#	print("nodes are already there")


#Prepare expression to put in tree with data.
#Try putting an array of complex numbers into tree.
#expr=Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", H, tH)
#n.putData(expr)

#Make nodes that get real and imaginary parts of transfer function for implementations of MDS interface which can't handle getting complex types.
#n.getNode('Hr').putData(Data.compile("real("+n.getPath()+")"))
#n.getNode('Hi').putData(Data.compile("aimag("+n.getPath()+")"))

#tree.write() #Write changes to tree

#print("Put data in "+n.getPath())

#This script shifts the current waveform by 50 ms so as to put it out of phase with the actual current signal.  The transfer function and coherence can then be recalculated to see whether resonances still appear.

from MDSplus import *
from myTools import *
import numpy

sFrom=1120814021
#sTo=1131014901
sTo=1131015901
#sFrom=1120926008
#sTo=1131015900

tree=Tree('magnetics',sFrom)
curNode=tree.getNode('shoelace.ant_i')
vcoNode=tree.getNode('shoelace.vco_freq')

iant,tiant=getYX(curNode)
fvco,tfvco=getYX(vcoNode)

tShift=0.050 #Shift time axis by this amount
t1=tiant[0]
tInd=numpy.argwhere(tiant>=(t1+tShift))[0][0]

#Rotate array circularly, shifting array backward by an amount of time, tShift
iant=numpy.concatenate( (iant[tInd:], iant[0:(tInd)]), 1 )

t1=tfvco[0]
tInd=numpy.argwhere(tfvco>=(t1+tShift))[0][0]

#Rotate array circularly, shifting array backward by an amount of time, tShift
fvco=numpy.concatenate( (fvco[tInd:], fvco[0:(tInd)]), 1 )

#Put shifted data into test shot.
tree=Tree('magnetics',sTo)
curNode=tree.getNode('shoelace.ant_i')
vcoNode=tree.getNode('shoelace.vco_freq')

expr=Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", iant, tiant) #Build a TDI expression for storing signal
curNode.putData(expr)

expr=Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", fvco, tfvco) #Build a TDI expression for storing signal
vcoNode.putData(expr)

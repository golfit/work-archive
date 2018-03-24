#CalcHilbertTrans.py
#This script opens up relevant nodes and drops in a hilbert transform for the signal.
#Ted Golfinopoulos, 23 Feb 2012
from MDSplus import *
from scipy import *
from scipy.signal import *
import sys

s=int(sys.argv[1])

tree=Tree('magnetics',s)

def calcHilb(parentNode) :
	y=parentNode.getData().data()
	yh=hilbert(y)
	timebase_expr='dim_of('+parentNode.getLocalPath()+')'  #Grab timebase with TDI expression so it's local - don't move over network.
	expr=Data.compile('BUILD_SIGNAL($1, *, '+timebase_expr+')', yh) #Build a TDI expression for storing signal.
	parentNode.getNode('hilbert').putData(expr)


calcHilb(tree.getNode('shoelace:ant_i'))
calcHilb(tree.getNode('shoelace:ant_v'))


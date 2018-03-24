#This script sets up nodes that will store the lookup table corner frequencies (these are lower-bound frequencies) for the series and parallel capacitors.
#
#Ted Golfinopoulos, 7 April 2015

import sys #For getting command line arguments
from MDSplus import *

if(len(sys.argv)>1) :
	s=int(sys.argv[1]) #Grab shot number from command line.
else :
	s=-1 #Default to shot -1

tree=Tree('Magnetics',s,'edit')

def tryAdd(parentNode, nodeName, nodeType ) :
    print("Trying to add "+nodeName+" under "+str(parentNode))
    try :
        parentNode.addNode(nodeName, nodeType)
        print("Added "+parentNode.getNode(nodeName))
    except Exception as inst:
        if(str(inst) != "%TREE-E-NODATA, No data available for this node") :
            print(inst)
            print("Can't add node, " + nodeName + " - may exist already.  Skipping")

print(tree)
myNode=tree.getNode('shoelace')
print(myNode)
tryAdd(myNode, 'mcb_lookup', 'Structure')

myNode=tree.getNode('shoelace.mcb_lookup')

tryAdd(myNode,'series_n_c','numeric')

tryAdd(myNode,'parallel_n_c','numeric')

tryAdd(myNode,'f_clk','numeric')
myNode.getNode('f_clk').putData(Data.compile('8.0D6')) #Clock frequency of MCB

tryAdd(myNode,'M','numeric')
myNode.getNode('M').putData(25) #Number of sync signal rising edges over which period is averaged over on MCB

tryAdd(myNode,'parallel_f_c','numeric')
myNode.getNode('parallel_f_c').putData(Data.compile( myNode.getNode('M').getPath() + " * " + myNode.getNode('f_clk').getPath() + " / "+ myNode.getNode('parallel_n_c').getPath()))

tryAdd(myNode,'series_f_c','numeric')
myNode.getNode('series_f_c').putData(Data.compile( myNode.getNode('M').getPath() + " * " + myNode.getNode('f_clk').getPath() + " / "+ myNode.getNode('series_n_c').getPath()))

tryAdd(myNode, 'comment','text')

tryAdd(myNode, 'last_updated','text')

#Write comment.
myNode.getNode('comment').putData('SERIES_N_C and PARALLEL_N_C are the lookup tables that specify the period counts (related inversely to the corner frequencies) for state changes determining which set of series and parallel capacitors are on.  If N is the total number of corner frequencies (with N+1 the total number of states), and i the index into an array of frequencies, then the state, s, is s=N-i, where capacitor levels 1 through to s will all be on at that state.  When s=0, all capacitors are switched out except the permanently-connected capacitors in the "baseload."  The arrays are arranged in order of increasing frequency (decreasing period).  If the frequency measured by the Master Control Board (MCB) is between indices, i-1 and i (s=N-i+1 and s=N-i), i.e. f_{i-1} <= f < f_{i}, then the MCB chooses the state associated with the upper frequency, f_{i}, and the lower state, s=N-i.  Note, however, that the MCB performs all calculations in terms of the period, as measured by an integer number of board clock counts.  The period is averaged over M rising edges from the "sync" signal, so for MCB clock frequency, f_clk, and period counts, n_clk, f_avg=1/tau_avg=M*f_clk/n_clk.  These values can be referenced in SERIES_F_C and PARALLEL_F_C.  All frequencies are in Hz.')

#Write new nodes to tree
tree.write()

print("Done adding MCB lookup table nodes to Shot "+str(s))

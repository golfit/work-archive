'''
This script sets up a corrected timebase node, and also an additional node that holds a flag determining whether the timebase has been corrected or not.

Ted Golfinopoulos, 22 June 2015
'''

from MDSplus import *
import sys #For getting command line arguments
import numpy
import myTools
import re


#Parse shot information, contained in first command-line argument
sList=myTools.parseList(sys.argv[1])

#List of nodes in remaining command line arguments

stringArgs=sys.argv[2:]

#Loop through shots in list
for s in sList :
    print("Shot {0:d}".format(s))

    #Open magnetics tree for editing to add new nodes.
    magTree=Tree('magnetics',s,'edit')

    #Try to add t_sig_source node - holds flag, 1=timebase corrected, 0=not corrected    
    try :
        magTree.getNode('shoelace.cpci.acq216_1').addNode('t_sig_source','numeric')
        magTree.getNode('shoelace.cpci.acq216_1.t_sig_source').putData(Data.compile('0')) #Default value is 0 - timebase has not been corrected yet.
    except :
        print('Could not add node, t_sig_source, for shot'+str(s)+' - may exist already')

    #Try to add timebase node - either points to corrected node or timebase of digitizer channel, based on t_sig_source node flag
    try :
        magTree.getNode('shoelace').addNode('timebase','axis')
        magTree.getNode('shoelace.timebase').putData(Data.compile('SHOELACE.CPCI:ACQ216_1:T_SIG_SOURCE ? \MAGNETICS::TOP.SHOELACE.CPCI:ACQ216_1:T_SIG_BASE : dim_of( SHOELACE.CPCI:ACQ216_1:INPUT_16 )')) #Default value is 0 - timebase has not been corrected yet.
    except :
        print('Could not add node, t_sig_source, for shot'+str(s)+' - may exist already')

    #Write the tree changes
    magTree.write()

    print('Finished added corrected timebase node and t_sig_source node for '+str(s))


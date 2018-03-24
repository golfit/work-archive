'''
This script changes the expression in the Shoelace pickup node to point to the timebase node.

Ted Golfinopoulos, 8 July 2015
'''

from MDSplus import *
import sys #For getting command line arguments
import numpy
import myTools
import re

#Parse shot information, contained in first command-line argument
sList=myTools.parseList(sys.argv[1])

#Loop through shots in list
for s in sList :
    print("Shot {0:d}".format(s))

    #Open magnetics tree for editing to add new nodes.
    magTree=Tree('magnetics',s)
    pickupNode=magTree.getNode('\MAGNETICS::TOP.SHOELACE:V_PICKUP:RAW')
    newExpr='Build_Signal(\MAGNETICS::TOP.SHOELACE.CPCI:ACQ216_1:INPUT_11, *, \MAGNETICS::TOP.SHOELACE:TIMEBASE)'
    pickupNode.putData(Data.compile(newExpr))

    #Try to add t_sig_source node - holds flag, 1=timebase corrected, 0=not corrected    
    try :
        pickupNode.putData(Data.compile(newExpr))
    except :
        print('Could not fix Shoelace pickup voltage timebase reference for shot '+str(s))

    print('Finished fixing Shoelace pickup voltage timebase reference for '+str(s))


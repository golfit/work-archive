from MDSplus import *
import myTools
import sys

#Add t_slow node for slow timebase for processed quantities
#T. Golfinopoulos, 1 April 2016 (April Fools' Day)

sList=myTools.parseList(sys.argv[1]) #Get shot from command line, first argument

for s in sList :
    try :
        myTree=Tree('magnetics',s,'edit')
        myTree.getNode('shoelace').addNode('t_slow','axis')
        myTree.getNode('shoelace.t_slow').addNode('comment','text')
        myTree.getNode('shoelace.t_slow.comment').putData("Slower timebase for processed quantities (amplitudes, powers, etc.).  The node is populated with an expression when the data processing script is run.  For backwards compatibility, the sampling frequency of this timebase ought to be 5 kHz (if the digitizer sampling frequency is 5 MHz).")
        myTree.write()
        
        print("Added node, SHOELACE.T_SLOW, to MAGNETICS tree for Shot "+str(s))
    except :
        print("Couldn't add T_SLOW node to SHOELACE subtree for Shot "+str(s))

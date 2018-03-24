'''
Created on May 17, 2013

@author: golfit
'''

from MDSplus import *
import numpy as np
import sys
import myTools as tools

##Parse shot information, contained in first command-line argument
#sList=tools.parseList(sys.argv[1])
#
#if(len(sList)) :
#    sList=[1130517900] #Default shot number

sList=[1130517900]

for s in sList :
    print("Creating Test Shot {0:d}".format(s)) #Print shot number
    tree=Tree('pcilocal',-1)
    tree.createPulse(s) #Create new pulse for this shot
    tree=Tree('pcilocal',s,'edit')
    myTree=Tree('pcilocal',s,'edit')
    print(myTree)
    #Grab node representations of hardware devices
    #Type is device, with hierarchy, subclass of object -> Data -> TreeNode -> Device
    
    decoderNode = myTree.getNode('ddecoder_1')
    jorwayTimingNode = myTree.getNode('jj221_1')
#    dig1Node=myTree.getNode('dt216b_1')
#    dig2Node=myTree.getNode('dt216b_2')
    
    #Init hardware
    decoderNode.doMethod('init')
    jorwayTimingNode.doMethod('init')
#    dig1Node.doMethod('init')
#    dig2Node.doMethod('init')
    print('Finished initing hardware')    

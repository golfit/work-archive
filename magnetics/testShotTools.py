'''
Created on May 20, 2013

@author: golfit
'''
from MDSplus.tree import Tree

#Function to grab parameters from PCI tree
def getPciParams(tree):
    tStart=tree.getNode('tstart').getData().evaluate()
    sampFreq=tree.getNode('input.sample_freq').getData().evaluate()
    inStart=tree.getNode('input:start').getData().evaluate()
    inLength=tree.getNode('input:length').getData().evaluate()
    inCStart=tree.getNode('input:c_start').getData().evaluate()
    inCLength=tree.getNode('input:c_length').getData().evaluate()
    inSBStart=tree.getNode('input:sb_start').getData().evaluate()
    inSBLength=tree.getNode('input:sb_length').getData().evaluate()
    
    return (tStart,sampFreq, inStart, inLength, inCStart, inCLength, inSBStart, inSBLength)

#Function to prepare a new PCI tree.
def makeNewPciTree(s): #s=shot number
    tree=Tree('pcilocal',-1)
    tStart,sampFreq, inStart, inLength, inCStart, inCLength, inSBStart, inSBLength=getPciParams(tree)
    tree.createPulse(s) #Create new pulse for this shot
    tree=Tree('pcilocal',s)
    tree.getNode('tstart').putData(tStart)
    tree.getNode('input.sample_freq').putData(sampFreq)
    tree.getNode('input:start').putData(inStart)
    tree.getNode('input:length').putData(inLength)
    tree.getNode('input:c_start').putData(inCStart)
    tree.getNode('input:c_length').putData(inCLength)
    tree.getNode('input:sb_start').putData(inSBStart)
    tree.getNode('input:sb_length').putData(inSBLength)

#    print('Created PCI tree for Shot {0:d}'.format(s))
    #Return new PCI tree.
    return tree

def makeNewMagTree(s):
    tree=Tree('magnetics',-1)
    tree.createPulse(s) #Create new pulse for magnetics tree for given shot
    
    #Grab new magnetics tree and return.
    return Tree('magnetics',s)
from MDSplus import *
import sys

if(len(sys.argv)<2) :
    s=-1 #Default shot number = model tree
else :
    s=int(sys.argv[1]) #Get shot number from command line

if(len(sys.argv)<3) :
    treeName='electrons' #Default tree name=electrons
else :
    treeName=sys.argv[2]

if(len(sys.argv)<4) :
    topNodeName='\ELECTRONS::TOP.REFLECT.CPCI:DT132_1' #Default top node
else :
    topNodeName=sys.argv[3]

#Open tree for editing
myTree=Tree(treeName,s,'edit')
#Get node under which new nodes will be added
topNode=myTree.getNode(topNodeName)

#Add nodes associated with timebase correction system
topNode.addNode('T_SIG_ACTION','action')
topNode.addNode('T_SIG_BASE','axis')
topNode.addNode('T_SIG_CHAN','signal')
topNode.addNode('T_SIG_DESC','text')
topNode.addNode('T_SIG_GATES','numeric')
topNode.addNode('T_SIG_START','numeric')
topNode.addNode('T_SIG_TIMES','signal')

myTree.write()

print("Added timebase correction nodes under "+(str(topNode.getFullPath()))+" for Shot "+str(s))

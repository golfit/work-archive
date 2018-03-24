from MDSplus import *
import sys
import myTools_no_sql as myTools

#Remove nodes, INPUT_##, where ## are the numbers, 17-24 (inclusive), which
#are erroneous pointers for reflectometer nodes.  Do so in the shoelace.cohere, shoelace.trans_fun,
#and shoelace.tfun_allfreq subtrees of the magnetics tree.

#Parse shot information, contained in first command-line argument
sList=myTools.parseList(sys.argv[1])

nodeNames=[]
count=0
for i in range(17,24+1) :
    nodeNames.append('INPUT_'+str(i))
    count=count+1
#reflectFreqs=['r50GHz', 'r60GHz', 'r75GHz', 'r88GHzlo', 'r88GHzhi', 'r112GHz','r132GHz','r140GHz']
#nodeNames=[]
#for i in range(0,len(reflectFreqs)) :
#	nodeNames.append(reflectFreqs[i]+'_amp')
#	nodeNames.append(reflectFreqs[i]+'_ang')

def removeNodes(topNode) :
    for i in range(0,len(nodeNames)) :
        try :
            print(topNode.getNode(nodeNames[i]).getFullPath())
            topNode.getNode(nodeNames[i]).delete()
        except :
            print("Can't remove "+str(nodeNames[i]))
            
for s in sList :
    myTree=Tree('magnetics',s,'edit')
    removeNodes(myTree.getNode('shoelace.cohere'))
    removeNodes(myTree.getNode('shoelace.trans_fun'))
    removeNodes(myTree.getNode('shoelace.tfun_allfreq'))
    print('Removed input_## nodes for Shot '+str(s))
    myTree.write()

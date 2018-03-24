#This script prints all of the EFIT nodes and their types with formatting to reconstitute the geqdsk and aeqdsk portions of the EFIT file
#T. Golfinopoulos, 17 May 2017

from MDSplus import *

s=1160607001

myTree=Tree('analysis',s)

def isChildOf(parent,child):
    '''
    USAGE:
        output=isChildOf(parent,child)
    
    @parent MDSplus node - check if this is the parent
    @child MDSplus node - check if this is the child
    @return true when child is descendant of parent, false otherwise
    '''
    parent_path=str(parent.getFullPath())
    child_path=str(child.getFullPath())
    return bool(child_path.find(parent_path)!=-1)

#In theory, get all sub nodes if this node.  In practice, this returns a much wider set of nodes, so filtering is needed.

def processTopNode(topNode):
    oldDefault=myTree.getDefault()
    myTree.setDefault(topNode)
    allSubNodes=topNode.getNodeWild('***')
    top_path=str(topNode.getFullPath())
    for n in allSubNodes :
        #print(n)
        if isChildOf(topNode,n) :
            #Path under sub node
            sub_path=str(n.getFullPath()).replace(top_path,'')[1:]
            node_usage=str(n.getUsage())
            print('topNode.addNode("'+sub_path+'","'+node_usage+'")')
            #Include comments
            if(node_usage=='TEXT'):
                try :
                    comment=str(n.getData().evaluate())
                    print("topNode.putData(Data.compile('$1'),'"+comment+"')")
                except :
                    print('#No data available in '+sub_path)
    myTree.setDefault(oldDefault) #Restore original default

#Process g_eqdsk
processTopNode(myTree.getNode('efit.results.g_eqdsk'))

print('#####DONE WITH G_EQDSK - MOVING TO A_EQDSK#####')
#Process a_eqdsk
processTopNode(myTree.getNode('efit.results.a_eqdsk'))
print('#####DONE WITH A_EQDSK#####')

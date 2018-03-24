from MDSplus import *

fromShot=1141009900 #Get data FROM this shot
toShot=-1 #Put data TO this shot

#Synchronize ALL nodes under this top node
topNodeName='shoelace.camac'

#Get all sub nodes of CAMAC structure
magTreeFrom=Tree('magnetics',fromShot)
topNodeFrom=magTreeFrom.getNode(topNodeName)
allSubNodesFrom=topNodeFrom.getNodeWild('***')

#Get sub nodes from tree that you desire to change
magTreeTo=Tree('magnetics',toShot)
topNodeTo=magTreeTo.getNode(topNodeName)
allSubNodesTo=topNodeTo.getNodeWild('***')

for i in range(0,len(allSubNodesFrom)) :
    toNode=magTreeTo.getNode(allSubNodesFrom[i].getFullPath())

    try :
        newExpr=allSubNodesFrom[i].getData().decompile()
    except :
        print("Can't extract expression from "+allSubNodesFrom[i].getFullPath()+" - skipping")
        continue

    try :
        toNode.putData(Data.compile(newExpr))
    except :
        print("Couldn't write data to "+toNode.getFullPath()+" - skipping")
        continue

    print(toNode.getFullPath())
    print(newExpr)
    print("---------------------------------------------------------")

print("Took data from Shot {0}".format(fromShot))
print("Done updating Shot {0}".format(toShot))

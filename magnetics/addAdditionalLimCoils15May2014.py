#This script whacks the MDSplus expressions in the tree to swap and turn and off nodes as the Shoelace antenna signals are migrated to a separate digitizer. 

#Include myTools module in path

from MDSplus import *
from numpy import *
import sys #For getting command line arguments
import re
sys.path.append("/home/golfit/python/versionControlled/trunk/qcm/myTools.py")
sys.path.append("/home/golfit/python/versionControlled/trunk/qcm/ChangeSpecificNodeExpr.py")


#s=1140513008 #Shot references to model tree
s0=1140515001
sEnd=1140515005
s=-1
#for s in range(s0,sEnd+1):
print("SHOT NUMBER "+str(s))
print("----------------------------------")

#Add nodes for BP24_GHK and BP23_GHK; give same expressions as BP16_GHK, and then adjust as appropriate
#Add nodes
try :
#    print("hello world")
#    myTree=Tree('magnetics',s,'edit')
#    sigNode=myTree.getNode('active_mhd.signals')
#    sigNode.addNode('bp17_ghk','signal')
#    myTree=Tree('magnetics',s,'edit')
#    sigNode=myTree.getNode('active_mhd.signals')
#    sigNode.addNode('bp24_ghk','signal')
#    sigNode.addNode('bp28_ghk','signal')
    #myTree=Tree('magnetics',s,'edit')
    #sigNode=myTree.getNode('active_mhd.signals')
    #sigNode.addNode('bp26_ghk','signal')
    #myTree=Tree('magnetics',s,'edit')
    #sigNode=myTree.getNode('active_mhd.signals')
    #sigNode.addNode('bp18_ghk','signal')
    myTree=Tree('magnetics',s,'edit')
    sigNode=myTree.getNode('active_mhd.signals')
    sigNode.addNode('bp19_ghk','signal')
    myTree.write() #Write changes to tree.
except :
    print("Couldn't add new nodes")



myTree=Tree('magnetics',s) #Fetch magnetics tree for model discharge.  None-edit mode.
refExpr=myTree.getNode('active_mhd.signals.bp16_ghk').getData().decompile()

#Give expression to BP17_GHK
myNode=myTree.getNode('active_mhd.signals.bp17_ghk')
newExpr=re.sub('BP\d\d_GHK','BP17_GHK',re.sub('ACQ_216_\d','ACQ_216_3',re.sub('INPUT_\d\d','INPUT_13',refExpr)))
newExpr=re.sub('CALIB\[\d\d\]','CALIB['+str(30+17-1)+']',newExpr) #Fix calibration num
myNode.putData(Data.compile(newExpr))
myNode.setOn(False) #Turn node off - it also seems noisy - made change in early hours of 16 May 2014
print("Node is "+str(myNode))
print("Expression for BP17_GHK is")
print(newExpr)

#Give expression to BP18_GHK
myNode=myTree.getNode('active_mhd.signals.bp18_ghk')
newExpr=re.sub('BP\d\d_GHK','BP18_GHK',re.sub('ACQ_216_\d','ACQ_216_3',re.sub('INPUT_\d\d','INPUT_13',refExpr)))
newExpr=re.sub('CALIB\[\d\d\]','CALIB['+str(30+18-1)+']',newExpr) #Fix calibration num
myNode.putData(Data.compile(newExpr))
myNode.setOn(False) #Turn node off - this coil is broken, it seems
print("Node is "+str(myNode))
print("Expression for BP18_GHK is")
print(newExpr)

#Give expression to BP19_GHK
myNode=myTree.getNode('active_mhd.signals.bp19_ghk')
newExpr=re.sub('BP\d\d_GHK','BP19_GHK',re.sub('ACQ_216_\d','ACQ_216_3',re.sub('INPUT_\d\d','INPUT_13',refExpr)))
newExpr=re.sub('CALIB\[\d\d\]','CALIB['+str(30+19-1)+']',newExpr) #Fix calibration num
myNode.putData(Data.compile(newExpr))
myNode.setOn(True) #Turn node off - this coil is broken, it seems
print("Node is "+str(myNode))
print("Expression for BP19_GHK is")
print(newExpr)

#Give expression to BP24_GHK
myNode=myTree.getNode('active_mhd.signals.bp24_ghk')
newExpr=re.sub('BP\d\d_GHK','BP24_GHK',re.sub('ACQ_216_\d','ACQ_216_3',re.sub('INPUT_\d\d','INPUT_14',refExpr)))
newExpr=re.sub('CALIB\[\d\d\]','CALIB['+str(30+24-1)+']',newExpr) #Fix calibration num
myNode.putData(Data.compile(newExpr))
myNode.setOn(True) #Turn node on
print("Node is "+str(myNode))
print("Expression for BP24_GHK is")
print(newExpr)

#Give expression to BP26_GHK
myNode=myTree.getNode('active_mhd.signals.bp26_ghk')
newExpr=re.sub('BP\d\d_GHK','BP26_GHK',re.sub('ACQ_216_\d','ACQ_216_1',re.sub('INPUT_\d\d','INPUT_16',refExpr)))
newExpr=re.sub('CALIB\[\d\d\]','CALIB['+str(30+26-1)+']',newExpr) #Fix calibration num
myNode.putData(Data.compile(newExpr))
myNode.setOn(True) #Turn node on
print("Node is "+str(myNode))
print("Expression for BP26_GHK is")
print(newExpr)

#Give expression to BP28_GHK
myNode=myTree.getNode('active_mhd.signals.bp28_ghk')
newExpr=re.sub('BP\d\d_GHK','BP28_GHK',re.sub('ACQ_216_\d','ACQ_216_3',re.sub('INPUT_\d\d','INPUT_15',refExpr)))
newExpr=re.sub('CALIB\[\d\d\]','CALIB['+str(30+28-1)+']',newExpr) #Fix calibration num
myNode.putData(Data.compile(newExpr))
myNode.setOn(True) #Turn node on
print("Node is "+str(myNode))
print("Expression for BP28_GHK is")
print(newExpr)

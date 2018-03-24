from MDSplus import *
import sys

shot=int(sys.argv[1])
newVoltageRange=sys.argv[2]
myTree=Tree('magnetics',shot)

boardNums=[1,2,3]
inputRange=range(1,16+1)

oldVoltageRange=myTree.getNode('active_mhd.data_acq.cpci.acq_216_2.input_01.vin').getData().evaluate()

for ii in boardNums :
    topNode=myTree.getNode('active_mhd.data_acq.cpci.acq_216_{0:d}'.format(ii))
    for inputNum in inputRange :
        vinNode=topNode.getNode('input_{0:02d}.vin'.format(inputNum))
        vinNode.putData(Data.compile(str(newVoltageRange)))

print('Changed voltage ranges for all three fast magnetics digitizers from '+format(oldVoltageRange)+' to '+newVoltageRange)

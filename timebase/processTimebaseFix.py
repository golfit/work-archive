'''
Created on May 28, 2013
Edited 10 June 2014 to reflect fact that fast magnetics now uses a single, master timebase for all three digitizers in service.

@author: golfit
'''

from MDSplus.tree import Tree
from fixTimebase import fixTimebase
from myTools import getShotRange
import MDSplus
import re

timebaseMasterBoard=3 #This is the board used as a timebase reference for all of the other boards.

def parseMagTimebaseNode( magTreeExpr ):
    digiNum=int(re.compile('DATA_ACQ.CPCI:.*_(\d{1,1}):INPUT_').findall(magTreeExpr)[0])
    #timeNode=magTree.getNode('active_mhd.data_acq.cpci.acq_216_{0:d}.t_sig_base'.format(digiNum))
    timeNode=magTree.getNode('active_mhd.data_acq.cpci.acq_216_{0:d}.t_sig_base'.format(timebaseMasterBoard))
    return digiNum, timeNode
                
#Grab sList from command-line arguments
sList=getShotRange()

nInputs=1

#Default trigger and sampling time offsets correcting nominal values, based on averages from surveys from existing corrected timebase versus nominal timebase data.
defaultT0ErrorMagAll=[1.96E-5,1.96E-5,1.96E-5]
defaultTsErrorMagAll=[5.663E-12, 7.404E-12, 6.010E-12]

#Replicate calibrated default errors from master board across all boards.
defaultT0ErrorMag=3*[defaultT0ErrorMagAll[timebaseMasterBoard-1]]
defaultTsErrorMag=3*[defaultTsErrorMagAll[timebaseMasterBoard-1]]


#Likewise, the average errors for PCI digitizer DT216B_1, which, as far as I know, shares its clock with DT216B_2
defaultT0ErrorPci=2.014E-5#0.4+4.2025E-5-(-0.3)-3500000*(200E-9+6.2513E-12)
defaultTsErrorPci=6.2513E-12
#defaultT0Pci=4.2025E-5
#defaultTsPci=6.2513E-12

numMagSigNodesFixed=0
numShoelaceNodesFixed=0
numPciNodesFixed=0

#For all shots in list
for s in sList :
    #Fix magnetics tree timebase
    try :
        magTree=Tree('magnetics',s)
    except :
        print("Can't open magnetics tree for Shot {0:d} - skipping")
        continue
    
    #Fix "Signals" nodes
    sigNodes=magTree.getNode('active_mhd.signals').getNodeWild('*')
    for sigNode in sigNodes :
        try :
            digiNum,timeNode=parseMagTimebaseNode(str(sigNode.getData().decompile()))
#            print(str(sigNode.getPath()))
#            print("digiNum={0:d}".format(digiNum))
#            fixTimebase(sigNode,timeNode,defaultT0ErrorMag[digiNum-1],defaultTsErrorMag[digiNum-1])
            fixTimebase(sigNode,timeNode) #Run without default timebase error correction so that if the code is run more than once, there will always be the same result.
            numMagSigNodesFixed+=1
        except :
            #Can't process the node - just skip it and keep going.
            print("Can't process {0:s}".format(str(sigNode.getPath())))
            continue
    
    print("Fixed {0:d} magnetics signals nodes so far - on to Shoelace nodes...".format(numMagSigNodesFixed))

    #Fix "Shoelace" nodes referencing the digitizer.
    #Use built-in list class, rather than TreeNodeArray to facilitate appending additional nodes. 
    shoelaceNodes=list(magTree.getNode('shoelace').getNodeWild('*'))
    #Append subnodes.
    shoelaceNodes=shoelaceNodes+list( magTree.getNode('shoelace').getNodeWild('***') )

    #Loop through all Shoelace nodes.  Find signal nodes which contain a pointer to a digitizer input channel.  Send these to fixTimebase.    
    for sigNode in shoelaceNodes :
        try :
            if(sigNode.getUsage()=="SIGNAL" and type(sigNode.record)==MDSplus.treenode.TreeNode) :
                if( re.compile("ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216").findall(str(sigNode.record)) ) :
                    digiNum,timeNode=parseMagTimebaseNode(str(sigNode.record))
#                    print(str(sigNode.getPath()))
#                    print("digiNum={0:d}".format(digiNum))
#                    fixTimebase(sigNode,timeNode,defaultT0ErrorMag[digiNum-1],defaultTsErrorMag[digiNum-1])
                    fixTimebase(sigNode,timeNode) #Run without default timebase erorr corrections
                    numShoelaceNodesFixed+=1
        except :
            #Can't process the node - just skip it and keep going.
            print("Can't process {0:s}".format(str(sigNode.getPath())))
            continue

    print("Fixed {0:d} shoelace nodes so far - on to PCI nodes...".format(numShoelaceNodesFixed))
    
#For all shots in list - loop separately for PCI tree because some shots may have magnetics trees but not PCI trees, or vice versa.
for s in sList :
    #Fix PCI tree timebase
    try :
        pciTree=Tree('pcilocal',s)
    except :
        print("Can't open magnetics tree for Shot {0:d} - skipping")
        continue
    
    #This timebase node either points to the nominal timebase, the corrected timebase, or the calibrated timebase. 
    timeNode=pciTree.getNode('results.timebase')
    #Grab all PCI "signal" nodes
    pciNodes=pciTree.getNode('results').getNodeWild('PCI*')
    for sigNode in pciNodes :
#        fixTimebase(sigNode,timeNode,defaultT0ErrorPci,defaultTsErrorPci)
        fixTimebase(sigNode,timeNode) #Run without default timebase error corrections.
        numPciNodesFixed+=1
        print("Fixed {0:s}".format(sigNode))
    print("...finished dt216b_1")
    
    print("Finished {0:d}".format(s))
    
    print("Fixed {0:d} PCI nodes so far - on to next shot, if there is one...".format(numPciNodesFixed))

print("Finished processing timebase fix")
print("Fixed a total of {0:d} magnetics signals nodes, {1:d} Shoelace nodes, and {2:d} PCI nodes".format(numMagSigNodesFixed, numShoelaceNodesFixed, numPciNodesFixed))

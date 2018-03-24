'''
Created on 8 Dec. 2015
1st modified: 8 Dec. 2015
2nd modified: 28 Sep. 2017

For fixing node references from BP09_ABK, BP11_ABK, and BP12_ABK, which were pointing to wrong digitizer (2 instead of 3) and to turn off BP20_ABK, which was not being digitized

28 Sep. 2017 - also turn off BP28_GHK, which is not connected at least for 2016 campaign

@author: golfit (Theodore Golfinopoulos)
'''

from MDSplus import *
from myTools import getShotRange
import sys
import re #Regular expressions

sList=getShotRange(int(sys.argv[1]))

#These Mirnov coils reference ACQ_216_2 instead of ACQ_216_3 - swap them
swapCoils=['bp09_abk','bp11_abk','bp12_abk']

#These Mirnov coils need to be turned off
#offCoils=['bp20_abk','bp28_ghk'] #28 Sep. 2017 - added BP28_GHK to list of nodes to turn off

appendage=['','.raw']

for s in sList :
    print('Shot '+str(s))
    magTree=Tree('magnetics',s)
    for thisCoil in swapCoils :
        for a in appendage:
            nodePath='active_mhd.signals.'+thisCoil+str(a)
            try :
                n=magTree.getNode(nodePath)
                oldExpr=str(n.getData().decompile())
                newExpr=oldExpr.replace('ACQ_216_2','ACQ_216_3')
                if( oldExpr != newExpr): #Only exchange expressions if different
                    n.putData( Data.compile( newExpr ) ) #Put new data into node
                    newExpr=n.getData().decompile()
                    print('Old expression: '+oldExpr)
                    print('New expression: '+newExpr)
            except :
                print("Can't get to "+nodePath+" - skipping)

#    for thisCoil in offCoils :
#        n=magTree.getNode('active_mhd.signals.'+thisCoil)
#        n.setOn(False)
#        print('Turned off'+n.getFullPath())

    print('')

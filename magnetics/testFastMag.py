'''
Created on March 15, 2015
Last modified: November 15, 2015

For running test shots on fast magnetics system.  Based on test script for Shoelace Antenna Power System.

@author: golfit (Theodore Golfinopoulos)
'''

from MDSplus import *
from MitDevices.acq216_ftp import ACQ216_FTP
from MitDevices.dt216b import DT216B
from MitDevices.acq216 import ACQ216
from testShotTools import makeNewMagTree, makeNewPciTree
import numpy as np
import sys

s=int(sys.argv[1])

print("Creating Test Shot {0:d}".format(s))

magTree=makeNewMagTree(s) #Build new magnetics tree for test shot, s

#Initialize CAMAC devices \MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CAMAC:MPB_DECODER
magTree.getNode('active_mhd.data_acq.camac:mpb_decoder').doMethod('init') #Need to init MPB first
magTree.getNode('active_mhd.data_acq.camac:j221').doMethod('init') #Need to init J221 timing sequence before the waveform generator, since the waveform gets its trigger from the J222 module connected to the J221 device.

#Pulled waveform generator from CAMAC crate in fast magnetics rack for use with Shoelace.  2 July 2015, T. Golfinopoulos
#magTree.getNode('active_mhd.data_acq.camac:waveform').doMethod('init') #The waveform generator should be inited after the devices which trigger it
magTree.getNode('ACTIVE_MHD.DATA_ACQ.CAMAC:C401_DECODER').doMethod('init') #Init instance to restart the global timebase synchronization device.

#Initialize CPCI devices - \MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_1
#magTree.getNode('ACTIVE_MHD.DATA_ACQ.CPCI:DIO2').doMethod('init')
print("Initing DIO2") #["MAGNETICS_START      ","START                "]
#magTree.getNode('\MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:DIO2').doMethod('init')
#magTree.getNode('\MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:DIO2.init_action').dispatch()
print("Skipping - triggering from MPB_DECODER")
print("Done initing DIO2")
my216Digis=[ACQ216(magTree.getNode('\MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_'+str(ii))) for ii in range(1,3+1)] #Cast digitizer node as acq216 device

def printAllStates(my216Digis) :
    '''
    Print state of all 216 digitizers.  Side-effect method.
    USAGE: printAllStates(my216Digis)
    INPUT: my216Digis - array of ACQ216 objects
    OUTPUT: None

    Ted Golfinopoulos, 15 March 2015
    '''
    ii=0
    for thisDigi in my216Digis :
        ii=ii+1
        print("Board "+str(ii)+" state = "+str(thisDigi.getBoardState()))
        #print(thisDigi.getstate(None)) #Old syntax - as of 21 Feb. 2016, there seems to be a getBoardState() method that works (see above)


#Loop through digitizers and init
for thisDigi in my216Digis :
    thisDigi.initftp() #Initialize device; the initftp method is also listed here: 

printAllStates(my216Digis) #Print states of digitizers

# ###################
# Wait - give time for board to init before running event - latency in init can cause board to miss trigger.
print("Waiting 7 seconds")
Data.execute('wait(7)')

printAllStates(my216Digis) #Print states of digitizers

# ###################
#Trigger start event
print("Triggering MAGNETICS_START event")
magTree.getNode('camac.hardware:encoder').doMethod("set_event","MAGNETICS_START")

printAllStates(my216Digis) #Print states of digitizers

#Call a wait before store.
print("Waiting 7 seconds")
Data.execute('wait(7)') #Wait - give time for experiment to run before storing.

printAllStates(my216Digis) #Print states of digitizers

#Store data
for thisDigi in my216Digis :
    thisDigi.store(None) #Not supposed to need to call an explicit store if autostore option is selected, which is the default behavior of initftp if no input is given.  However, the data was not getting stored without this call, while it did get stored with it.  See 1141125903

printAllStates(my216Digis) #Print states of digitizers

print("----------------------------------")
print("Test shot finshed and stored under")
print(s)
print("----------------------------------")

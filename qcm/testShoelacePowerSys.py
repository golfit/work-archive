'''
Created on October 9, 2014
Last modified: November 25, 2014

For running test shots on components in Shoelace Antenna Power System rack.

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

#Initialize CAMAC devices
magTree.getNode('shoelace.camac:mpb_decoder').doMethod('init') #Need to init MPB first
magTree.getNode('shoelace.camac:j221').doMethod('init') #Need to init J221 timing sequence before the waveform generator, since the waveform gets its trigger from the J222 module connected to the J221 device.
magTree.getNode('shoelace.camac:waveform').doMethod('init') #The waveform generator should be inited after the devices which trigger it

#Initialize CPCI devices
my216Digi=ACQ216(magTree.getNode('\MAGNETICS::TOP.SHOELACE.CPCI:ACQ216_1')) #Cast digitizer node as acq216 device
my216Digi.initftp() #Initialize device; the initftp method is also listed here: \MAGNETICS::TOP.SHOELACE.CPCI:ACQ216_1:INIT_ACTION - if no input is given, the board will autostore
print("Board state = "+str(my216Digi.getBoardState())) #16 March 2016 getstate no longer works - use getBoardState now.
#print("Board state = ")
#print(my216Digi.getstate(None)) #Removed 16 March 2016 TG

print("Waiting 7 seconds")
Data.execute('wait(7)') #Wait - give time for board to init before running event - latency in init can cause board to miss trigger.

print("Board state = "+str(my216Digi.getBoardState())) #16 March 2016 getstate no longer works - use getBoardState now.
#print("Board state = ")
#print(my216Digi.getstate(None))

#Trigger start event
print("Triggering MAGNETICS_START event")
magTree.getNode('camac.hardware:encoder').doMethod("set_event","MAGNETICS_START")
print("Board state = "+str(my216Digi.getBoardState())) #16 March 2016 getstate no longer works - use getBoardState now.
#print("Board state = ")
#print(my216Digi.getstate(None))

#Call a wait before store.
print("Waiting 7 seconds")
Data.execute('wait(7)') #Wait - give time for experiment to run before storing.

print("Board state = "+str(my216Digi.getBoardState())) #16 March 2016 getstate no longer works - use getBoardState now.
#print("Board state = ")
#print(my216Digi.getstate(None))

#Store data
my216Digi.store(None) #Not supposed to need to call an explicit store if autostore option is selected, which is the default behavior of initftp if no input is given.  However, the data was not getting stored without this call, while it did get stored with it.  See 1141125903

print("Board state = "+str(my216Digi.getBoardState())) #16 March 2016 getstate no longer works - use getBoardState now.
#print("Board state = ")
#print(my216Digi.getstate(None))

print("----------------------------------")
print("Test shot finshed and stored under")
print(s)
print("----------------------------------")
#Currently, nothing to store - no digitizers installed as of 9 October 2014

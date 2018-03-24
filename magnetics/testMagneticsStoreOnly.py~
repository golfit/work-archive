'''
Created on May 23, 2013

@author: golfit
'''

from MDSplus import *
from MitDevices.acq216_ftp import ACQ216_FTP
from MitDevices.dt216b import DT216B
#import numpy as np
import sys

s=int(sys.argv[1])

#Repopen magnetics tree
print("Storing magnetics data...")
magTree=Tree('magnetics',s)
ACQ216_FTP(magTree.getNode('active_mhd.data_acq.cpci:acq_216_1')).storeftp(None)
ACQ216_FTP(magTree.getNode('active_mhd.data_acq.cpci:acq_216_2')).storeftp(None)
ACQ216_FTP(magTree.getNode('active_mhd.data_acq.cpci:acq_216_3')).storeftp(None)
print('...done storing magnetics data')

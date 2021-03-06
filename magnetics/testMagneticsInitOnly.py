'''
Created on May 23, 2013

@author: golfit
'''

from MDSplus import *
from MitDevices.acq216_ftp import ACQ216_FTP
from MitDevices.dt216b import DT216B
from testShotTools import makeNewMagTree, makeNewPciTree
#import numpy as np
import sys

s=int(sys.argv[1])

#Setup and init magnetics tree.
magTree=makeNewMagTree(s)
magTree.getNode('active_mhd.data_acq.camac:mpb_decoder').doMethod('init')
magTree.getNode('active_mhd.data_acq.camac:j221').doMethod('init')
magTree.getNode('active_mhd.data_acq.camac:waveform').doMethod('init')
magTree.getNode('active_mhd.data_acq.camac:waveform2').doMethod('init')
magTree.getNode('active_mhd.data_acq.camac:amhd_a12').doMethod('init')
magTree.getNode('active_mhd.data_acq.camac:c401_decoder').doMethod('init')

magTree.getNode('active_mhd.data_acq.cpci:dio2').doMethod('init')

ACQ216_FTP(magTree.getNode('active_mhd.data_acq.cpci:acq_216_1')).initftp(None)
ACQ216_FTP(magTree.getNode('active_mhd.data_acq.cpci:acq_216_2')).initftp(None)
ACQ216_FTP(magTree.getNode('active_mhd.data_acq.cpci:acq_216_3')).initftp(None)
#    ACQ216_FTP(magTree.getNode('active_mhd.data_acq.cpci:dio2')).init(None)
#ACQ216_FTP(magTree.getNode('active_mhd.data_acq.cpci:dio2')).initftp(None)

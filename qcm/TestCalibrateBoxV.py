#TestCalibrateBoxV.py
#This function loads some uncalibrated voltage data from one of the I/V boxes and applies the calibration.
#Ted Golfinopoulos, 3 Feb 2012

from MDSplus import *
from calibrateBoxV import *

s=1120105018

tree=Tree("magnetics", s, 'edit')

tree.setDefault(tree.getNode('shoelace:ant_v'))

dataNode=tree.getNode('raw')

#Grab data and convert to native data type
v=dataNode.getData().data() #Raw voltage
t=dataNode.getData().dim_of().data()

#Calibrate
boxID=2 #The antenna box is #2.
vc=calibrateBoxV( v, t, boxID )

#Make a node to store calibrated data
tree.addNode('calibrated', 'signal')
tree.write()

#Put calibrated data into tree.
expr=Data.compile("BUILD_SIGNAL($VALUE, $1, $2)", vc, t) #Build a TDI expression for storing signal
tree.getNode('calibrated').putData(expr)



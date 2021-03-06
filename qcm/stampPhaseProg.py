#04-Sep-2015 - Control string for \MAGNETICS::TOP.SHOELACE:PH_PROGRAM:PHASE_DEG Shoelace antenna - autogenerated from genPythonStampFun.m

from MDSplus import *
from numpy import array

tree=Tree("magnetics",-1)
expr=Data.compile("BUILD_SIGNAL([-180.0000, -180.0000, 180.0000, -180.0000, 180.0000, -180.0000,  180.0000],*,[-0.1000000, 0.5000000, 0.7500000, 1.0000000, 1.2500000, 1.5000000,  4.0000000])")
tree.getNode("\MAGNETICS::TOP.SHOELACE:PH_PROGRAM:PHASE_DEG").putData(expr)

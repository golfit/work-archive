#This script sets up nodes in specified trees (or the model tree) for the phase delay system.
#Ted Golfinopoulos, 25 September 2012
from MDSplus import *

s=-1

#tree=Tree('magnetics',s,'edit') #Open model tree for editing.
tree=Tree('magnetics',s) #Open model tree for editing.

topNode=tree.getNode('shoelace.ph_program')

#Add nodes to tree.
#topNode.addNode('phase_deg','signal')
#topNode.addNode('phase_wave','signal')
#topNode.addNode('comment','text')

phaseDegNode=topNode.getNode('phase_deg')
phaseWaveNode=topNode.getNode('phase_wave')
#Put in default values for programming and calibration.

topNode.getNode('comment').putData('Nodes for phase delay control.  phase_deg = phase delay in degrees, signal with values from -180 to +180. phase_wave = programming voltage used by BiRa')
phaseDegNode.putData(Data.compile("Build_Signal($1, *, $2)", [0.0, 0.0], [-0.1, 4.0]))
phaseWaveNode.putData(Data.compile("Build_Signal("+phaseDegNode.getFullPath()+"*10./180., *, dim_of("+phaseDegNode.getFullPath()+"))",))

#Change waveform in programming node of BiRa to point to calibrated programming node.
tree.getNode('active_mhd.data_acq.camac.waveform2.channel_4.programming').putData(Data.compile(phaseWaveNode.getFullPath()))

#Write changes to tree
#tree.write()

#Old expression in active_mhd.data_acq.camac.waveform2.channel_4.programming
#Build_Signal(0. * [0.,0.,-10.,10.,-10.,0.,0.], *, [0.,0.,.5,1.,1.5,2.,4.])

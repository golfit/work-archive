#TurnOffMagNodes.py
#This script opens the Active MHD signals tree and turns off nodes whose digitizer inputs are being retasked to Shoelace signals.
#Ted Golfinopoulos, 17 Feb 2012
from MDSplus import *
import re


digitizer='ACQ_216_2' #Digitizer inputs which are affected
inputs=[1,2,3,4,5,6,9] #Turn these Mirnov coil inputs off for the specified digitizer

#Regular expression pattern specifying affected nodes
#The r prefix before the quotes requires Python to interpret the string as a "raw" string literal, avoiding issues as needing to double backslashes.
pattern=r'ACQ_216_2:INPUT_0[1-69]' #Note this is numbers 1 to 6 OR 9, not 1 to 69.

tree=Tree('magnetics', -1)
tree.setDefault(tree.getNode('active_mhd.signals')) #Go into signals node.
nodes=tree.getNodeWild('***')

for n in nodes :
	try :
		if ( re.findall(pattern,str(n.getData())) and n.isOn()) :
			#n.setOn(False) #Turn node off.
			print('I would turn off: '+n.getPath())
	except TreeNoDataException :
		print('No data in node '+n.getPath()+'; moving on.')

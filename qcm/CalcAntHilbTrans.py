#This script calculates the Hilbert transform of the antenna current and puts it in the tree.
#Ted Golfinopoulos, 7 June 2012
from numpy import *
from scipy.fftpack import *
from MDSplus import *
import re
import sys #For getting command line arguments

#Parse command line arguments.
if(len(sys.argv)>1) :
	s1=int(sys.argv[1]) #Grab shot number from command line.
else :
	print("Hilbert Transform Calc: Must supply a shot number.")

if(len(sys.argv)>2) :
	s2=int(sys.argv[2]) #Grab shot number from command line.
else :
	s2=s1 #Only do a single shot

#Loop through range of shots
if(s2>=s1 and s1>0) :
	for s in range(s1,s2+1) :
		tree=Tree('magnetics',s)
		#Grab data and convert to native data type
		dataNode=tree.getNode('shoelace.ant_i')
		try :
			outNode=tree.getNode('shoelace.ant_i.hilb')
			try :
				ia=dataNode.getData().evaluate().data() #Antenna current, dc component removed and calibrated. [A]
				#t=dataNode.getData().evaluate().dim_of().data() #Time axis [s]
				#Calculate Hilbert transform and put into tree.
				#For some reason, Hilbert transform in Python is -1*Hilbert transform in Matlab - make consistent with Matlab's convention.
				#Build a TDI expression for storing signal.
				expr=Data.compile("BUILD_SIGNAL($VALUE, $1, dim_of("+dataNode.getFullPath()+"))", -hilbert(ia))
				outNode.putData(expr)
				print("Put Hilbert transform of current signal in shoelace.ant_i.hilb for {0:d}".format(s))
			except :
				print("Couldn't process Shoelace antenna current data for {0:d} - skipping.".format(s))
		except :
			print("Couldn't get shoelace.ant_i.hilb node for {0:d} - skipping.".format(s))

else :
	print("Hilbert Transform Calc: shot range must be > 0, and in increasing order.")

	

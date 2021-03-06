#SwapDigitizerNumber.py
#This script swaps the tree references associating coil signal lines with a particular digitizer.  When ACQ_216_1 died, we had to move the coils to ACQ_216_3.  Now that ACQ_216_1 is resurrected, we need to switch the references back.
#
#Usage:
#	python SwapDigitizerNumber.py [s1 [s2]]
#
#	Default: Shot -1 (model tree)
#	range between shots s1 and s2, including s1 and s2.
#Ted Golfinopoulos, 25 Apr 2012

from MDSplus import *
import sys #For getting command line arguments
import re #Import regular expressions.

#Parse command line arguments.
if(len(sys.argv)>1) :
	s1=int(sys.argv[1]) #Grab shot number from command line.
else :
	s1=-1 #Default to shot -1

if(len(sys.argv)>2) :
	s2=int(sys.argv[2]) #Grab shot number from command line.
elif(s1==-1) :
	s2=s1 #If s1 is the model tree, only do s=-1; don't run to s=0
else :
	s2=s1 #Only do a single shot

digFrom='ACQ_216_3' #Change digitizer from this
digTo='ACQ_216_1' #Change digitizer to this

#Loop through range of shots
for s in range(s1,s2+1) :
	tree=Tree('magnetics',s)
	nodeArr=tree.getNode('active_mhd.signals').getNodeWild('BP*') #Grab all shoelace subnodes

	#Loop through all nodes
	for n in nodeArr :
		#print(n)
		try :
			expr=n.getData()
			#print(str(expr))
			try :
				if (len(re.findall(digFrom, str(expr)))>0) :#If there are matches, replace old digitizer name with new.
					newExpr=re.sub(digFrom, digTo, str(expr)) #Need to to-string expression in order for regular expression to work.
					#print(str(n) + ' -> ' + str(newExpr))
					n.putData(Data.compile(newExpr)) #Put new expression into node.
					print( str(n)+" --- Now contains: "+str(n.getData()) )
			except : print("String replacement didn't work.  Expr was "+str(expr))
		except TreeNoDataException :
			#Continue
			print("No data in "+n.getPath()+"; moving on.")

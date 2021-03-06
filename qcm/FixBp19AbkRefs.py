#This script changes the expression for the BP19_ABK signal node when it pointed to a non-existent node (missing pointer to CPCI in reference).
#Ted Golfinopoulos, 27 April 2012
from MDSplus import *
import re
import sys #For getting command line arguments

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

subExprFrom='DATA_ACQ.ACQ_216_2' #Change digitizer from this
subExprTo='DATA_ACQ.CPCI:ACQ_216_2' #Change digitizer to this

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
				if (len(re.findall(subExprFrom, str(expr)))>0) :#If there are matches, replace old digitizer name with new.
					subExprTo=re.sub(digFrom, digTo, str(expr)) #Need to to-string expression in order for regular expression to work.
					#print(str(n) + ' -> ' + str(newExpr))
					n.putData(Data.compile(newExpr)) #Put new expression into node.
					print( str(n)+" --- Now contains: "+str(n.getData()) )
			except : print("String replacement didn't work.  Expr was "+str(expr))
		except TreeNoDataException :
			#Continue
			print("No data in "+n.getPath()+"; moving on.")

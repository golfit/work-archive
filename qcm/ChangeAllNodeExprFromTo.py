#This script reads to changes the expression for the BP19_ABK signal node when it pointed to a non-existent node (missing pointer to CPCI in reference).
#Ted Golfinopoulos, 27 April 2012
from MDSplus import *
import re
import sys #For getting command line arguments

#Parse command line arguments.
if(len(sys.argv)>3) :
	s1=int(sys.argv[3]) #Grab shot number from command line.
else :
	s1=-1 #Default to shot -1

if(len(sys.argv)>4) :
	s2=int(sys.argv[4]) #Grab shot number from command line.
elif(s1==-1) :
	s2=s1 #If s1 is the model tree, only do s=-1; don't run to s=0
else :
	s2=s1 #Only do a single shot

if(len(sys.argv)>1) :
	subExprFrom=sys.argv[1]
else :
	print("Must enter a sub expression to change from")
	s1=0
	s2=-1

if(len(sys.argv)>2) :
	subExprTo=sys.argv[2]
else :
	print("Must enter a sub expression to change to")
	s1=0
	s2=-1

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
					newExpr=re.sub(subExprFrom, subExprTo, str(expr)) #Need to to-string expression in order for regular expression to work.
					#print(str(n) + ' -> ' + str(newExpr))
					n.putData(Data.compile(newExpr)) #Put new expression into node.
					print( str(n)+" --- Now contains: "+str(n.getData()) )
			except : print("String replacement didn't work.  Expr was "+str(expr))
		except TreeNoDataException :
			#Continue
			print("No data in "+n.getPath()+"; moving on.")

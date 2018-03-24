#This script reads in a from-to replacement string pair and applies the changes to a specified node for a specified shot range.
#Ted Golfinopoulos, 8 May 2012
from MDSplus import *
import re
import sys #For getting command line arguments
import myTools 


#Parse command line arguments.
if(len(sys.argv)>4) :
	#Parse shot information, contained in first command-line argument
	sList=myTools.parseList(sys.argv[4])
else :
	sList=-1 #Default to shot -1

if(len(sys.argv)>6) :
	treeName=sys.argv[5] #Name of tree
else :
	treeName='magnetics' #Default tree name

if(len(sys.argv)>1) :
	node=sys.argv[1]
else :
	print("Must enter a valid node name in magnetics tree")
	s1=0
	s2=-1

if(len(sys.argv)>2) :
	subExprFrom=sys.argv[2]
else :
	print("Must enter a sub expression to change from")
	s1=0
	s2=-1

if(len(sys.argv)>3) :
	subExprTo=sys.argv[3]
else :
	print("Must enter a sub expression to change to")
	s1=0
	s2=-1

#Loop through range of shots
for s in sList :
	print(s)
	tree=Tree(treeName,s)
	n=tree.getNode(node)

	try :
		expr=n.getData()
		print(str(expr))
		print(subExprFrom)
		print(subExprTo)
		try :
			print(len(re.findall(subExprFrom, str(expr)))>0)
			if (len(re.findall(subExprFrom, str(expr)))>0) :#If there are matches, replace old digitizer name with new.
				newExpr=re.sub(subExprFrom, subExprTo, str(expr)) #Need to to-string expression in order for regular expression to work.
				#print(str(n) + ' -> ' + str(newExpr))
				n.putData(Data.compile(newExpr)) #Put new expression into node.
				print( str(n)+" --- Now contains: "+str(n.getData()) )
		except : print("String replacement didn't work.  Expr was "+str(expr))
	except TreeNoDataException :
		print('TreeNoDataException')
		#Continue
		print("No data in "+n.getPath()+"; moving on.")

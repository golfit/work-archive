#changeTreeRefs.py
from MDSplus import *
import re

#This script opens the Shoelace subtree in the model tree and replaces instances of pointers to one digitizer, digFrom, with references to another, digTo.
#@param expr String (i.e. MDSplus expression) to process
#@param digFrom String specifying digitizer name to change from.  Can also be a regular expression.
#	@param digTo String specifying digitizer name to change to.
#
#	@return expression string, expr, with replacements made.

#	Ted Golfinopoulos, 17 Feb 2012

#Make regular expression
#	return re.sub(digFrom, digTo, expr)

digFrom='ACQ_216_3'
digTo='ACQ_216_2'

tree=Tree('magnetics',-1)
nodeArr=tree.getNode('shoelace').getNodeWild('***') #Grab all shoelace subnodes

#Go through Shoelace subnodes; look for instances of references to old digitizer, and replace with instances to new digitizer.  Handle cases where nodes do not contain expressions.
for n in nodeArr :
	try :
		expr=n.getData();
		try :
			if (len(re.findall(digFrom, str(expr)))>0) :#If there are matches, replace old digitizer name with new.
				newExpr=re.sub(digFrom, digTo, str(expr)) #Need to to-string expression in order for regular expression to work.
				n.putData(Data.compile(newExpr)) #Put new expression into node.
				print(n.getPath()+" --- Now contains: "+n.getData())
		except : print("String replacement didn't work.  Expr was "+expr)
	except TreeNoDataException :
		#Continue
		print("No data in "+n.getPath()+"; moving on.")

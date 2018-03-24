#This script is meant to fix the digitizer inputs associated with several Mirnov coils whose pointer expressions were for the wrong digitizer.  This problem seems to exist from 2014 forward
#Ted Golfinopoulos, 25 September 2017 (Dad's 63 birthday)
from MDSplus import *
import re
import sys #For getting command line arguments
import myTools 

#OLD INPUT NUMS:
#ACQ_216_2:INPUT_09 -> BP09_ABK
#ACQ_216_2:INPUT_11 -> BP11_ABK
#ACQ_216_2:INPUT_12 -> BP12_ABK

#NEW INPUT NUMS
#ACQ_216_3:INPUT_09 -> BP09_ABK
#ACQ_216_3:INPUT_11 -> BP11_ABK
#ACQ_216_3:INPUT_12 -> BP12_ABK 

#Dictionaries: map coil name to old and new expressions
#ab_coil_names=['BP09_ABK','BP11_ABK','BP12_ABK']
old_input_names={'BP09_ABK':'ACQ_216_2:INPUT_09','BP11_ABK':'ACQ_216_2:INPUT_11','BP12_ABK':'ACQ_216:INPUT_12'}
new_input_names={'BP09_ABK':'ACQ_216_2:INPUT_09','BP11_ABK':'ACQ_216_2:INPUT_11','BP12_ABK':'ACQ_216:INPUT_12'}

#Parse command line arguments.
if(len(sys.argv)>1) :
	#Parse shot information, contained in first command-line argument
	sList=myTools.parseList(sys.argv[1])
else :
	sList=-1 #Default to shot -1

treeName='magnetics'

#Loop through range of shots
for s in sList :
	print("Shot "+str(s))
	tree=Tree(treeName,s)

	for coil_name in old_input_names.keys() :
	    #Change both top node and raw node references for coil, if necessary, since some coil nodes might not point to raw or calib
	    try :
	        n_list=[tree.getNode('active_mhd.signals.'+coil_name),tree.getNode('active_mhd.signals.'+coil_name+'.raw')]
	    except :
	        n_list=[tree.getNode('active_mhd.signals.'+coil_name)]
		for n in n_list:
		    subExprFrom=old_input_names[coil_name]
		    subExprTo=new_input_names[coil_name]
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

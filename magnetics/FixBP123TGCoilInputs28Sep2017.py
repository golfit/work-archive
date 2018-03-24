#This script is meant to fix the digitizer inputs associated with several Mirnov coils whose leads were cut during repairs in the last opening
#Ted Golfinopoulos, 28 Sep. 2017
#The same fix seems to apply for 2014, 2015, and 2016 campaigns
from MDSplus import *
import re
import sys #For getting command line arguments
import myTools 

#OLD INPUT NUMS:
#ACQ_216_1:INPUT_07 -> BP3T_GHK
#ACQ_216_1:INPUT_08 -> BP2T_GHK
#ACQ_216_1:INPUT_09 -> BP1T_GHK

#NEW INPUT NUMS
#ACQ_216_1:INPUT_07 -> BP1T_GHK
#ACQ_216_1:INPUT_08 -> BP2T_GHK
#ACQ_216_1:INPUT_09 -> BP3T_GHK 

#CORRECT OVERALL SIGNS:
#ACQ_216_1:INPUT_07 -> -1
#ACQ_216_1:INPUT_08 -> +1
#ACQ_216_1:INPUT_09 -> +1

#old_input_nums=[9,7,8] or [8,9,7]
new_input_nums=[7,8,9] #ACQ_216_1 inputs corresponding to BP1T_GHK, BP2T_GHK, and BP3T_GHK

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

	if(s<1140000000 and s != -1) :
		print("Shot before 2014 - skipping")
		continue

	for coil_num in range(1,3+1) :
		n=tree.getNode('active_mhd.signals.bp{0:d}t_ghk'.format(coil_num))
		subExprFrom='INPUT_0\d'
		subExprTo='INPUT_0{0:d}'.format(new_input_nums[coil_num-1])
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

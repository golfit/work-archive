#This script whacks the MDSplus expressions in the tree to swap and turn and off nodes as the Shoelace antenna signals are migrated to a separate digitizer. 

#Include myTools module in path

from MDSplus import *
from numpy import *
import sys #For getting command line arguments
import re
sys.path.append("/home/golfit/python/versionControlled/trunk/qcm/myTools.py")
sys.path.append("/home/golfit/python/versionControlled/trunk/qcm/ChangeSpecificNodeExpr.py")


#s=1140513008 #Shot references to model tree
s0=1140513001
sEnd=1140513008
sRange=range(s0,sEnd+1)

for s in sRange :
#	s=-1
	print("SHOT NUMBER "+str(s))
	print("----------------------------------")

	myTree=Tree('magnetics',s) #Fetch magnetics tree for model discharge

	#digiFrom='ACQ16_1'
	#digiTo='ACQ_216_3'
	#digiFrom='DATA_ACQ:ACQ_216_3'
	#\MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3
	#digiFrom='DATA_ACQ:ACQ16_FTP1'
	digiFrom='DATA_ACQ:ACQ16_1|DATA_ACQ:ACQ16_FTP1|DATA_ACQ.CPCI:MHD_ACQ216_2'
	digiTo='DATA_ACQ.CPCI:ACQ_216_3'

	#Loop through all BP\d\d_ABK nodes.
	for coilNum in range(1,12+1) :
	    nodeName='active_mhd.signals.bp{0:02d}_abk'.format(coilNum)
	    print(nodeName)
	    try :
		myNode=myTree.getNode(nodeName)
		myExpr=myNode.getData().decompile()
	#        print(myExpr)

		#Change digitizer name.
		try :
		    print(len(re.findall(digiFrom, str(myExpr)))>0)
		    if (len(re.findall(digiFrom, str(myExpr)))>0) :#If there are matches, replace old digitizer name with new.
		        newExpr=re.sub(digiFrom, digiTo, str(myExpr)) #Need to to-string expression in order for regular expression to work.
		        myNode.putData(Data.compile(newExpr)) #Put new expression into node.
		        myExpr=myNode.getData().decompile() #Grab new expression.
	#                print( str(nodeName)+" --- Now contains: "+str(myNode.getData().decompile()) )
		except :
		    print("String replacement didn't work.  Expr was "+str(myExpr))

	    except :
		print("Cannot access node "+nodeName+" - skipping")

	    #Change channel number.
	    newExpr=re.sub('INPUT_\d\d','INPUT_{0:02d}'.format(coilNum),myExpr) #Replace instances of input with correct channel number
	    myNode.putData(Data.compile(newExpr)) #Put new expression into node.
	    myExpr=myNode.getData().decompile() #Grab new expression.
	#    print( str(nodeName)+" --- Now contains: "+str(myNode.getData().decompile()) )

	    #Replace CALIB_K with CALIB
	    newExpr=re.sub('CALIB_K','CALIB',myExpr)
	    myNode.putData(Data.compile(newExpr)) #Put new expression into node.
	    myExpr=myNode.getData().decompile() #Grab new expression.
	    print( str(nodeName)+" --- Now contains: "+str(myNode.getData().decompile()) )

	    #Change calib reference
	    newExpr=re.sub('CALIB[\d{1,2}]','CALIB[{0:d}]'.format(coilNum-1),myExpr)
	    myNode.putData(Data.compile(newExpr)) #Put new expression into node.
	    myExpr=myNode.getData().decompile() #Grab new expression.
	    print( str(nodeName)+" --- Now contains: "+str(myNode.getData().decompile()) )

	    #Eliminate KAMP_GAINS multiplier, which multiplies with the calibration factor.  I think it is obsolete.
	    newExpr=re.sub('\\\\MAG_RF_FLUCT:KAMP_GAINS\[\d+\]','1.0',myExpr)
	    myNode.putData(Data.compile(newExpr)) #Put new expression into node.
	    myExpr=myNode.getData().decompile() #Grab new expression.
	    print( str(nodeName)+" --- Now contains: "+str(myNode.getData().decompile()) )

	    #Make sure check on coil status is for correct coil
	    newExpr=re.sub('GETNCI(BP\d\d_ABK, "ON")','GETNCI(BP{0:02d}_ABK, "ON")'.format(coilNum),myExpr)
	    myNode.putData(Data.compile(newExpr)) #Put new expression into node.
	    myExpr=myNode.getData().decompile() #Grab new expression.
	    print( str(nodeName)+" --- Now contains: "+str(myNode.getData().decompile()) )


	    #Turn node on, unless 10; then, leave off
	    if(coilNum != 10) :
		myNode.setOn(True)

	#Change antenna pickup node
	myNode=myTree.getNode('shoelace.v_pickup.raw')
	newExpr=re.sub('INPUT_\d\d','INPUT_10',myNode.getData().decompile())
	myNode.putData(Data.compile(newExpr))
	myExpr=myNode.getData().decompile() #Grab new expression
	print(str(myNode)+" --- Now contains: "+str(myExpr))

	myNode=myTree.getNode('active_mhd.signals.qcm_pickup.raw')
	newExpr=re.sub('INPUT_\d\d','INPUT_10',myNode.getData().decompile())
	myNode.putData(Data.compile(newExpr))
	myExpr=myNode.getData().decompile() #Grab new expression
	print(str(myNode)+" --- Now contains: "+str(myExpr))


	#Turn off BP01_GHK
	myNode=myTree.getNode('active_mhd.signals.bp01_ghk')
	myNode.setOn(False) #Turn off node

	#Move BP05_GHK to ACQ_216_2:INPUT_01 and turn on
	myNode=myTree.getNode('active_mhd.signals.bp05_ghk')
	#Swap input and digitizer of node
	newExpr=re.sub('ACQ_216_\d','ACQ_216_2',re.sub('INPUT_\d\d','INPUT_01',myNode.getData().decompile()))
	myNode.putData(Data.compile(newExpr))
	#Turn node on
	myNode.setOn(True)
	myExpr=myNode.getData().decompile() #Grab new expression
	print(str(myNode)+" --- Now contains: "+str(myExpr))

	#Turn on BP16_GHK and give Channel=ACQ_216_3:INPUT_13
	myNode=myTree.getNode('active_mhd.signals.bp16_ghk')
	#Swap input and digitizer of node
	newExpr=re.sub('BP\d\d_GHK','BP16_GHK',re.sub('ACQ_216_\d','ACQ_216_3',re.sub('INPUT_\d\d','INPUT_13',myNode.getData().decompile())))
	myNode.putData(Data.compile(newExpr))
	#Turn node on
	myNode.setOn(True)
	myExpr=myNode.getData().decompile() #Grab new expression
	print(str(myNode)+" --- Now contains: "+str(myExpr))

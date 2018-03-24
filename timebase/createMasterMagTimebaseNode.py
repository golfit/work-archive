'''
Created 10 June 2014
Add a master timebase node to the tree

Modified 29 March 2016 - reference corrected timebase for each individual digitizer, rather than master timebase, since ACQ216's apparently skip initial samples on occasion. -Ted Golfinopoulos
'''

from MDSplus import *
import sys 

shot=int(sys.argv[1])

#Open magnetics tree for editing
myTree=Tree('magnetics',shot,'edit')

topNode=myTree.getNode('active_mhd.signals')

#Add master timebase node as axis.
digiNums=[1,2,3]
for i in range(0,len(digiNums)) :
    try :
        #Try to add timebase node.
        topNode.addNode('timebase','axis')
        timebaseNode=topNode.getNode('timebase') #Retrieve new node
        #ACQ_216_3 is master digitizer in and after 2014
        nodeExpression='if_error( \MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3:T_SIG_BASE, dim_of(\MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3:INPUT_16))'
        #The calling sequence, myNode.putData(Data.compile(myTdiStr)), was broken by an "improvement" to MDSplus around 6 Oct. 2017
        timebaseNode.putData(myTree.tdiCompile(nodeExpression))
        #Write changes to tree
        myTree.write()
    except:
        print("Couldn't add timebase node to tree - may already exist")
    
    try :
        topNode.addNode('timebase'+str(digiNums[i]),'axis')
        timebaseNode=topNode.getNode('timebase'+str(digiNums[i])) #Retrieve new node

        #Stamp expression into timebase node which defaults to timebase of acq_216_3:input_16, where timebase synchronization signal goes, but switches to \MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3:T_SIG_BASE when it is available.
        #The if_error() MDSplus TDI function evaluates expressions until it no longer encounters an error, and returns the result of the first error-free expression in the series of expressions, or the last error if all expressions have errors.
        #Modified 29 March 2016 - change from ACQ_216_3 to timebase for each individual digitizer, sinc ACQ216's can skip initial samples on occsion. -Ted Golfinopoulos
        #nodeExpression='if_error( \MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_'+str(digiNums[i])+':T_SIG_BASE, dim_of(\MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_'+str(digiNums[i])+':INPUT_16))'
        #Modified 28 September 2017 - retain pointer to corrected time base for each individual digitizer, but point default to TIMEBASE node, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE
        nodeExpression='if_error( \MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_'+str(digiNums[i])+':T_SIG_BASE, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE)'
        timebaseNode.putData(myTree.tdiCompile(nodeExpression))

        #Write changes to tree
        myTree.write()

        print("Added node, "+str(timebaseNode)+", for Shot {0:d}".format(shot))
    except :
        print("Couldn't add timebase node for Digitizer Number "+str(digiNums[i]))

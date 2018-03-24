'''
Created on May 27, 2013

@author: golfit
'''
from MDSplus.mdsdata import Data
import MDSplus
import re

def parseAllTimebaseParams(myExpr):
    parseRegExpr=re.compile("Build_Dim\(Build_Window\((.+), (.+), (.+)\), \* : \* : (.+)\)+")
    subStrings=parseRegExpr.findall(myExpr)
    indStart=subStrings[0][0]
    indEnd=subStrings[0][1]
    t0=subStrings[0][2]
    ts=subStrings[0][3]
    return indStart, indEnd, t0, ts

def parseTimebaseExpr(myExpr):
    #Get all doubles out of expression
    allParams=parseAllTimebaseParams(myExpr)
    
    #Try to parse start and sampling times from timebase string.  If cannot,
    #try to execute string as TDI expression.
    try :
        myNums=[float(re.compile("D").sub("E",myStr)) for myStr in allParams[2:(3+1)]]
        t0=myNums[0]
        ts=myNums[1]
    except :
        t0=float(Data.execute(str(allParams[2])))
        ts=float(Data.execute(str(allParams[3])))
    return t0, ts #Return the trigger time and the sampling time

def extractTimebaseExpr(myExpr):
    '''
    Extract the "dimension" timebase from the signal expression in signalNode.
    '''
    #Look for Build_Dim(Build_Window( calls and return whole segment
    myPattern=re.compile("Build_Dim\(Build_Window\(.*\),[^)]*\){1,1}")
    return myPattern.findall(myExpr)[0]

def fixTimebase( signalNode, timebaseNode, defaultT0Error=None, defaultTsError=None ):
    '''
    Function to point signal node to corrected timebase, or, failing that, to optionally add
    default error corrections to the nominal timebase.
    
    USAGE:
        fixTimebase( signalNode, timebaseNode, defaultT0Error=None, defaultTsError=None )
    
    INPUT:
        signalNode = MDSplus tree node which contains a TDI signal expression
        timebaseNode = MDSplus tree node which contains the corrected timebase (via a TDI expression)
        defaultT0Error = correction to ADD to nominal start (trigger) time.  By default, don't change the nominal trigger time
        defaultTsError = correction to ADD to the nominal sampling time (1/sampling frequency).  By default, don't change the nominal sampling time.
    
    OUTPUT:
        none
    
    Ted Golfinopoulos
    27 May 2013 (created)
    '''
    
    if( defaultT0Error is None or defaultTsError is None ) :
        noDefaultVals=True
    elif( abs(defaultT0Error)>0.1 or abs(defaultTsError)>1E-10 ) :
        print("Default t0 or ts error is too large - don't apply default correction")
        noDefaultVals=True
    else :
        noDefaultVals=False
    
    isBadCorrectedTimebase=False

    #Grab nominal timebase parameters for comparison with corrected values
    try :
        sig=signalNode.record.evaluate() #Extra evaluate is needed, for example, when the expression is wrapped in code that only returns a signal when the node is ON.
        t0Nom=sig.getDimensions()[0].evaluate().getWindow().evaluate().getTimeAt0().evaluate()
        tsNom=sig.getDimensions()[0].evaluate().getAxis().evaluate().getDelta().evaluate()
    except Exception,e:
        print("Skipping - couldn't access given signal node, {0:s}- error was {1:s}".format(str(signalNode), str(e)))
        return
    
    #Extract trigger and sample times from corrected timebase to see whether they are realistic.
    try :
        tsigDim=timebaseNode.record.evaluate()
        #tsigDim=timebaseNode
        t0Corrected=tsigDim.evaluate().getWindow().evaluate().getTimeAt0().evaluate()
        tsCorrected=tsigDim.evaluate().getAxis().evaluate().getDelta().evaluate()
        
        
        #Check absolute values of corrected timebase to make sure they are realistic
        if( abs(t0Corrected)>10. or tsCorrected<0. or tsCorrected>1.E-3 ) :
            print("Corrected timebase had bad parameters, t0={0:3.10g} and ts={1:3.10g} - skipping".format(float(t0Corrected), float(tsCorrected)))
            isBadCorrectedTimebase=True
        
        #Check to make sure corrected timbase parameters are not too far from nominal values
        #- if they are, there is probably a problem.
        if( abs(t0Corrected-t0Nom)>0.1 or abs(tsCorrected-tsNom)/tsNom>1.E-2 ) :
            print("Nominal timebase parameters: t0={0:5.10G} s, ts={0:5.10G} s".format(float(t0Nom),float(tsNom)))
            print("Corrected timebase parameters: t0={0:5.10G} s, ts={0:5.10G} s".format(float(tsCorrected),float(tsCorrected)))
            print("Discrepancy too large")
            isBadCorrectedTimebase=True #Exit
    except :
        isBadCorrectedTimebase=True

    changeDim=False

    if( not isBadCorrectedTimebase ) :
        #Replace dimension in old signal expression with pointer to corrected timebase.
        myNewDim=Data.compile(timebaseNode.getPath())
        changeDim=True

    else : #Bad corrected timebase
        if(noDefaultVals) :
            print("Bad corrected timebase and no useable default errors - no changes made to signal node.")
            return
        else :
            print("Using default timebase error corrections")
            myNewDim=sig.getDimensions()[0].evaluate()
            myNewDim.getWindow().setTimeAt0(t0Nom+defaultT0Error)
            myNewDim.getAxis().setDelta(tsNom+defaultTsError)
            changeDim=True

    if(changeDim) :
        myData=signalNode.record
        
        if( type(myData)==MDSplus.compound.Function ) :
            if( type(myData.getArguments()[0])==MDSplus.compound.Signal ) :
                myArgs=myData.getArguments()
                myArgs[0].setDimensions(tuple([myNewDim]))
                myData.setArguments(myArgs)
                
        elif( type( myData )==MDSplus.compound.Signal ) :
            myData.setDimensions(tuple([myNewDim]))
            
        elif( type( myData )==MDSplus.treenode.TreeNode ) :
            newSig=Data.compile('Build_Signal(*,*,*)')
            newSig.setValue(Data.compile("DATA($VALUE)"))
            newSig.setRaw(myData)
            newSig.setDimensions(tuple([myNewDim]))
            myData=newSig
        else :
            print("Input node is neither a function nor a signal nor a tree node reference; don't know how to make fix.  No changes made.")
            return
        
#        print(myData.record)
#        print(myData)
        signalNode.record=myData #Put in corrected data.
    
    else :
        print("No changes made to {0:s}".format(str(signalNode.getPath())))
    
        
#        print(   "t0New="+str(t0Nom)+re.compile("e").sub( "D", "+{0:5.10g}".format(defaultT0Error)) \
#              +", tsNew="+str(tsNom)+re.compile("e").sub( "D", "+{0:5.10g}".format(defaultTsError)))
#        signalNode.write_once=False
#        signalNode.record=sig #Replace sig with new instance of sig.
#        signalNode.writeOnce=True


#            indStart,indEnd,t0Str,tsStr=parseAllTimebaseParams(nomTimebaseExpr)
            #Create new timebase string.  Make sure to express doubles with "D" instead of "e".
#            newDimStr="Build_Dim(Build_Window("+indStart+", "+indEnd+", {0:10.15f}".format(t0Nom+defaultT0Error)+re.compile("e").sub( "D","), * : * : {0:5.15g})".format(tsNom+defaultTsError))
#	signalNode.write_once=False

#	signalNode.writeOnce=True

#    if(not(newDimStr is None)) :
#        dimPattern=re.compile("Build_Dim\(Build_Window\(.*\),[^)]*\){1,1}")
#        newExpr=dimPattern.sub(str(newDimStr),str(oldExpr))        
#        signalNode.write_once=False
#        signalNode.record=newExpr
#        signalNode.write_once=True
#        print("No expression: "+newExpr)
#    else :
#        print("No changes made to signal node expression.")

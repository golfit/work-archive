#This script processes the transfer function between the Shoelace antenna current and pickup signals (e.g. Mirnov coils, etc.)
#Ted Golfinopoulos, 13 June 2012

from MDSplus import *
import sys #For getting command line arguments
import numpy
import myTools_no_sql as myTools
from scipy.fftpack import hilbert
from scipy.interpolate import interp1d
import re
#from calcTransFun import *


#Parse shot information, contained in first command-line argument
sList=myTools.parseList(sys.argv[1])

#List of nodes in remaining command line arguments

stringArgs=sys.argv[2:]

#Loop through shots in list
for s in sList :
    print("Shot {0:d}".format(s))

    #Open magnetics tree to get Shoelace antenna signal.
    magTree=Tree('magnetics',s, 'edit')

    if(s<1110000000 and s>0) : antNode=magTree.getNode('active_mhd.signals:i_gh_upper_z') #Old current node for Active MHD antenna - for comparison with Jason Sears' work.
    else : antNode=magTree.getNode('shoelace.ant_i') #Shoelace antenna current node.

    #Check to see if antenna current node is on - if it is not, skip and continue.
    if(not(antNode.isOn())):
        print("Antenna current node is off for Shot {0:d} - skip and continue".format(s))
        continue

    usePremadeListFlag=False #Flag to indicate whether user has specified a premade list of nodes, or has entered them explicitly at the command line.
    nodeList=[] #Initialize variable to hold paths of list of "output signal" nodes - calculate transfer function for these signals.

    nodeList,ceceNodes=myTools.parsePremadeNodeList(stringArgs, s)

    if(len(nodeList)>0) : usePremadeListFlag=True

    #Calculate cross-correlation component if requested.
    if( any([x=="crosscorr" for x in stringArgs]) or any([x=="mscohere" for x in stringArgs]) ) : crossCorrFlag=True
    else : crossCorrFlag=False

    if(not(usePremadeListFlag)) :
        nodeList=stringArgs #Otherwise, user has specified list of signals, explicitly.

    #Loop through nodes for which transfer function is desired
    for nodeName in nodeList :
        #Parse tree name
        extractTreeName=re.findall('(\\\)(.{1,12})(::)',nodeName)
        if(len(extractTreeName)==0) :
            sigTree=magTree #Default tree is magnetics
            treeName='magnetics'
        else :
            treeName = extractTreeName[0][1] #Second argument from regular expression output is tree name
            print(treeName)
            sigTree=Tree(treeName,s)

        #If nodeName is actually a TDI signal expression, and not a single node path, treat accordingly.
        if( re.match( 'build_signal', str(nodeName).lower() ) or treeName.lower()=='cmod' ) :
            nodeExpr=nodeName
            #If reflectometer channel, have to change node name based on index.
            if len(re.findall('input_(\d\d)',str(nodeName).lower())) != 0 :
                reflectFreqs=['R50GHz', 'R60GHz', 'R75GHz', 'R88GHzlo', 'R88GHzhi', 'R112GHz','R132GHz','R140GHz']
                reflectList=[]
                for i in range(0,len(reflectFreqs)) :
                    reflectList.append(reflectFreqs[i]+'_amp')
                    reflectList.append(reflectFreqs[i]+'_ang')
                    reflectList.append(reflectFreqs[i]+'_cos')
                    reflectList.append(reflectFreqs[i]+'_sin')
                
                #Parse reflectometer index from input
                digiInput=int(re.findall('input_(\d\d)',str(nodeName).lower())[0])
                freqIndex=int((digiInput-1)*0.5) #Parse index into reflectFreqs from input digitizer (1 or 2 => 0, 3 or 4 => 1, etc.)
                if(len(re.findall('_amp',str(nodeExpr).lower()))!=0) : #Amplitude string
                    probeName=reflectList[freqIndex*4] #*4 because there are four reflectometer processing options, amp, phase angle, cos, sin
                elif(len(re.findall('arg',str(nodeExpr).lower()))!=0) : #Phase string
                    probeName=reflectList[freqIndex*4+1]
                elif(len(re.findall('_acos',str(nodeExpr).lower()))!=0) : #cos string
                    probeName=reflectList[freqIndex*4+2]
                else : #sin string
                    probeName=reflectList[freqIndex*4+3]
            elif len(re.findall('.*gpi.*',str(nodeName).lower())) != 0 :
                #Parse GPI chord index from TDI expression
                #chordIndices=re.findall('(\d{1,2}),(\d{1,2})',str(nodeName).lower())
                chordIndices=[int(x) for x in re.findall('(\d{1,2}),(\d{1,2})',str(nodeName).lower())[0]]
                print(chordIndices)
                probeName='gpi_'+str(chordIndices[0])+'_'+str(chordIndices[1])
            else :
                print("Node name="+str(nodeName)+", don't know how to handle this expression - skipping and continuing")
        else :             
            sigNode=sigTree.getNode(nodeName)
            probeName=sigNode.getNodeName() #Grab name of node.
            if(treeName.lower()=='magnetics') :
                nodeExpr=str(sigNode.getFullPath()).lower().replace(treeName.lower(),'cmod').replace('top.','top.mhd.'+treeName.lower()+'.')
            else :
                nodeExpr=str(sigNode.getFullPath()).lower().replace(treeName.lower(),'cmod').replace('top.','top.'+treeName.lower()+'.')
            print(nodeExpr)
            #See if node is on; if it is off, skip and go to next.
            if( not(sigNode.isOn()) ) :
                print("Node, "+str(sigNode.getPath())+" is off; skipping and continuing")
                continue

        #Add up and down to names of ASP probes.
        if( re.search('.UP:',nodeName) ) : probeName=probeName+"UP"
        elif( re.search('.DN:',nodeName ) ) : probeName=probeName+"DN"
        elif( re.search('.P0:',nodeName ) ) : probeName="P0_"+probeName
        elif( re.search('.P1:',nodeName ) ) : probeName="P1_"+probeName
        elif( re.search('.P2:',nodeName ) ) : probeName="P2_"+probeName
        elif( re.search('.P3:',nodeName ) ) : probeName="P3_"+probeName
        
        #Shorten name of density node so that it fits in 12-character MDSplus limit.
        probeName=probeName.lower().replace('density_fit','ne_fit')

        if(s<1110000000 and s>0) : topNode=magTree.getNode('active_mhd')
        else : topNode=magTree.getNode('shoelace')

        try :
            #Add new tree node to hold transfer functions
            topNode.addNode('trans_fun','structure')

            #Write changes to tree.
            magTree.write()
        except :
            print("...can't add trans_fun structure node - may exist already")

        transFunNode=topNode.getNode('trans_fun')

        try :
            #Add a node for each coil
            transFunNode.addNode(str(probeName),'signal')

            #Add sub-nodes for node.
            n=transFunNode.getNode(str(probeName))
            
            n.addNode('raw','signal')
            n.addNode('Hr','signal')
            n.addNode('Hi','signal')

            #Write changes to tree.
            magTree.write()
        except :
            n=transFunNode.getNode(str(probeName))
            print("...transfer function subnodes for "+probeName+" are already there")

        n=transFunNode.getNode(probeName)
        n.getNode('raw').putData(Data.compile(nodeExpr)) #Add expression with pointer (from CMOD tree) to raw data node.

        print("Made transfer function nodes in "+n.getPath()+" for Shot {0:d}".format(s))

        #######################Cross-coherence
        if( crossCorrFlag ) :
            try :
                #Add new tree node to hold cross-coherence
                topNode.addNode('mscohere','structure')

                #Write changes to tree.
                magTree.write()
            except :
                print("...can't add mscohere structure node - may exist already")

            mscohereNode=topNode.getNode('mscohere')

            try :
                #Add a node for each coil
                mscohereNode.addNode(probeName,'signal')

                #Add sub-nodes for node.
                n=mscohereNode.getNode(probeName)
            
                n.addNode('raw','signal')

                #Write changes to tree.
                magTree.write()
            except :
                n=mscohereNode.getNode(probeName)
                print("...magnitude squared coherence subnodes for "+probeName+" are already there")

            print("Added magnitude square coherence nodes in "+n.getPath()+" for Shot {0:d}".format(s))

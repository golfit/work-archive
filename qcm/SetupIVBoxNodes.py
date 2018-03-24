#SetupSpareIVBoxNode.py
#This script puts a node for the spare I/V box in the Shoelace subtree with appropriate calibration nodes.
#Ted Golfinopoulos, 7 March 2015
#Based on original script from 15 Mar 2012

import sys #For getting command line arguments
from MDSplus import *

if(len(sys.argv)>1) :
	s=int(sys.argv[1]) #Grab shot number from command line.
else :
	s=-1 #Default to shot -1

tree=Tree('Magnetics',s,'edit')

#All nodes are signal nodes
#Tuplet data order is (node_name, box_number, comment, default_calibration)
parentNodes=[('ant_v',3,'Antenna voltage',200.09),('ant_i',3,'Antenna current',-100.0),('match_v',4,'Voltage looking into matching network',198.29),('match_i',4,'Current looking into matching network',100.0),('src2_v',2,'Voltage out of Source 2',198.45),('src2_i',2,'Current out of Source 2',100.0),('src_v',1,'Voltage out of Source 1',198.96),('src_i',1,'Current out of Source 1',100.0),('spare_v',5,'Voltage over spare capacitive voltage divider board',200.42),('spare_i',5,'Current through spare current monitor',10.0),('v_pickup',6,'Voltage induced over antenna when in passive pickup (receiver) mode',1.0)]
#default_calibrations=[200.09, 100.0, 198.29, 100.0, 198.45, 100.0, 198.96, 100.0]

def tryAdd(parentNode, nodeName, nodeType ) :
    print("Trying to add "+nodeName)
    try :
        parentNode.addNode(nodeName, nodeType)
        print("Added "+parentNode.getNode(nodeName))
    except Exception as inst:
        print(inst)
        print("Can't add node, " + nodeName + " - may exist already.  Skipping")

def setupNode(tree,nodeName,boxNum, comment, cal) :
    #Try to add the voltage or current node.
    tryAdd( tree.getNode('shoelace'), nodeName, 'signal' )

    node=tree.getNode('shoelace.'+nodeName)
    
    #All subnodes for this node - pairs/triplets are (node_name, node_type[, parent_node])
    nodesToAdd=[('comment','text'),('raw','signal'),('cal','numeric'),('box_num','numeric'),('calibrated','signal'),('cal_vs_freq','signal'),('H_real','numeric','cal_vs_freq'),('H_imag','numeric','cal_vs_freq'),('H_imag','numeric','cal_vs_freq'),('freq_axis','numeric','cal_vs_freq'),('comment','text','cal_vs_freq')]

    #Default value for node - used fixed, real, scalar calibration
    node.putData(Data.compile(node.getPath()+':raw * '+node.getPath()+':cal'))

#    tree.setDefault(node)	

    #Add nodes - change parent node from default, if necessary.
    for ii in range(0, len(nodesToAdd) ) :
        baseNode=node
        if( len(nodesToAdd[ii])==3 ) :
            baseNode=node.getNode(nodesToAdd[ii][2])
        print("Base node = "+str(baseNode))
        tryAdd(baseNode,nodesToAdd[ii][0],nodesToAdd[ii][1])

    #Put data in nodes
    node.getNode('cal').putData(cal) #Default scalar calibration
    node.getNode('comment').putData(comment) #Default comment

#Tuplet data order is (node_name, box_number, comment, default_calibration)
for ii in range(0,len(parentNodes)) :
    setupNode(tree,parentNodes[ii][0],parentNodes[ii][1],parentNodes[ii][2],parentNodes[ii][3])
    print("-----------------------------")

#Write changes to tree
tree.write()

print("Done adding I/V box nodes")

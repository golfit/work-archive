from MDSplus import *
import myTools
import sys

#Add match_v_amp, match_i_amp, match_pwr, match_zr, and match_zi nodes
#T. Golfinopoulos, 1 April 2016 (April Fools' Day)

sList=myTools.parseList(sys.argv[1]) #Get shot from command line, first argument

for s in sList :        
    try :
        myTree=Tree('magnetics',s,'edit')
        myTree.getNode('shoelace').addNode('match_v_amp','signal')
        myTree.getNode('shoelace.match_v_amp').addNode('comment','text')
        myTree.getNode('shoelace.match_v_amp.comment').putData("Amplitude of voltage looking into matching network, on load-side of transformers.")
        
        myTree.getNode('shoelace').addNode('match_i_amp','signal')
        myTree.getNode('shoelace.match_i_amp').addNode('comment','text')
        myTree.getNode('shoelace.match_i_amp.comment').putData("Amplitude of current looking into matching network, on load-side of transformers.")
        
        myTree.getNode('shoelace').addNode('match_pwr','signal')
        myTree.getNode('shoelace.match_pwr').addNode('comment','text')
        myTree.getNode('shoelace.match_pwr.comment').putData("Powering entering into matching network on load-side of transformers.")
        
        myTree.getNode('shoelace').addNode('match_zr','signal')
        myTree.getNode('shoelace.match_zr').addNode('comment','text')
        myTree.getNode('shoelace.match_zr.comment').putData("Real part of complex impedance looking into matching network, on load-side of transformers.")

        myTree.getNode('shoelace').addNode('match_zi','signal')
        myTree.getNode('shoelace.match_zi').addNode('comment','text')
        myTree.getNode('shoelace.match_zi.comment').putData("Imaginary part of complex impedance looking into matching network, on load-side of transformers.")
        
        myTree.write()
        
        print("Added match_v_amp, match_i_amp, match_pwr, match_zr, and match_zi nodes to MAGNETICS tree, SHOELACE subtree for Shot "+str(s))
    except :
        print("Couldn't add T_SLOW node to SHOELACE subtree for Shot "+str(s))

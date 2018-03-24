from MDSplus import *
from myTimebaseSignature import timeSignature
import sys 

shot=int(sys.argv[1])
#shot=1130523900

nBoards=1

path='dt216b_1'
print "processing shot %d" % (shot,)
t = Tree('pcilocal', shot)
print "  Fixing %s " %(path,)
p = t.getNode(path)
if p.getNode('t_sig_chan').length == 0 :
	if node[-7:-1] == 'DT132_' :
	    p.getNode('t_sig_chan').record = p.getNode('input_16')
	else :
	    print("No timebase sync channel available")
if(shot<1130000000) : #Use a smaller discriminator for older PCI
	(sig_base, sig_times) = timeSignature(p,0.1)
else :
	(sig_base, sig_times) = timeSignature(p) #Use default discriminator
p.getNode('t_sig_base').record = sig_base
p.getNode('t_sig_times').record = sig_times
try :
	p.getNode('t_sig_source').record = 1
except:
	print "      no t_sig_source node"

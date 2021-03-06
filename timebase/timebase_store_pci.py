from MDSplus import *
from pciTimebaseSignature import timeSignature

#Use a smaller discriminator for edge detection, since PCI uses
#somewhat-broken channel to record global timebase signal
#Ted Golfinopoulos, 10 June 2014
discriminator=0.1

def timebase_store(shot, path) :
    print "processing shot %d" % (shot,)
    t = Tree('cmod', shot)
    print "  Fixing %s " %(path,)
    p = t.getNode(path)
    if p.getNode('t_sig_chan').length == 0 :
	if node[-7:-1] == 'DT132_' :
	    p.getNode('t_sig_chan').record = p.getNode('input_07') #Note that PCI uses Channel 7 on first board for timebase input
	else :
	    return
    (sig_base, sig_times) = timeSignature(p,discriminator)
    p.getNode('t_sig_base').record = sig_base
    p.getNode('t_sig_times').record = sig_times
    try :
	p.getNode('t_sig_source').record = 1
    except:
	print "      no t_sig_source node"

from MDSplus import *
from MitDevices import timeSignature
import sys 

shot=int(sys.argv[1])

nBoards=3

for boardNum in range(1,nBoards+1) :
	print(boardNum)
	print('test{0:d}'.format(boardNum))
	path='ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_{0:d}'.format(boardNum)
	print "processing shot %d" % (shot,)
	t = Tree('magnetics', shot)
	print "  Fixing %s " %(path,)
	p = t.getNode(path)
	if p.getNode('t_sig_chan').length == 0 :
		if node[-7:-1] == 'DT132_' :
		    p.getNode('t_sig_chan').record = p.getNode('input_16')
		else :
		    continue
	(sig_base, sig_times) = timeSignature(p)
	p.getNode('t_sig_base').record = sig_base
	p.getNode('t_sig_times').record = sig_times
	try :
		p.getNode('t_sig_source').record = 1
	except:
		print "      no t_sig_source node"

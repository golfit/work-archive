'''
Created on May 30, 2013

Correct (a) voltage calibration in magnetics, (b) PCI timebase and t_sig_base (if possible), and (c) timebase references
in "signal" nodes of magnetics and PCI trees. 

@author: golfit
'''
from myTools import getShotRange
from myTools import getYX
import datetime
import sys
from MDSplus import *
from numpy import logical_and
from numpy import mean
from numpy import max

#s1=1080000000
#s2=1121002899
#s1=1080321020
#s2=1080321030
#s1=1120000000
#s2=1121002899
s1=1080000000
s2=1090000000
sList=getShotRange(s1,s2)

t1=0.5
t2=1.5

rgapCutoff=1.2 #Maximum rgap average
nl04Cutoff=1.2E20 #Minimum nl04 density (proxy for H-mode) level 

for s in sList :
	try :
		#Fetch RGAP data
		t=Tree('analysis',s)
		n=t.getNode('\ANALYSIS::EFIT_AEQDSK:Oright')
		rgap,trgap=getYX(n)

		t=Tree('electrons',s);
		nl04,tnl04 = getYX(t.getNode('tci.results:nl_04'));

		if( mean(rgap[logical_and(trgap>=t1,trgap<=t2)])<rgapCutoff and max( nl04[logical_and(tnl04>=t1,tnl04<=t2)] )>nl04Cutoff ) :
			#If shot might show an EDA on magnetics, record it in log
			myLogFile=open('/home/golfit/python/versionControlled/trunk/qcm/ShotsWithHmodeAndSmallGap.txt','a')
			myLogFile.write('{0:d}\n'.format(s))
			myLogFile.close()
	except :
		print('Could not process Shot {0:d}'.format(s))
	

print('Done with shot range, {0:d}-{1:d}'.format(s1,s2))

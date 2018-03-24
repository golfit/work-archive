'''
Created on May 23, 2013

@author: golfit
'''
from MDSplus.tree import Tree
import sys
import re #Regular expressions

def parseExpr(myExpr):
	#Get all doubles out of expression
	getNumExpr=re.compile("(-*\d*\.\d+D*-*\d*)")
	dblsAsStrings=getNumExpr.findall(myExpr)
	#Cast strings as floating point numbers
	myNums=[float(re.compile("D").sub("E",str)) for str in dblsAsStrings]
	t0=myNums[0]
	ts=myNums[1]
	return t0, ts #Return the trigger time and the sampling time

s=int(sys.argv[1]) #Get shot number

fname="/home/golfit/python/versionControlled/trunk/qcm/timebaseErrorSurvey.txt"

#Put in sentinel values for start and sampling times.
t0=[-1.,-1.,-1.,-1.]
ts=[-1.,-1.,-1.,-1.]

magTree=Tree('magnetics',s) #Get magnetics tree
for digiNum in range(1,4):
	myPath="active_mhd.data_acq.cpci.acq_216_{0:d}.t_sig_base".format(digiNum)
	#Get start time and sampling time
	t0[digiNum-1],ts[digiNum-1]=parseExpr(magTree.getNode(myPath).getData().decompile())
	
try :
	pciTree=Tree('pcilocal',s) #Get PCI tree
	myPath="dt216b_1.t_sig_base"
	t0[3],ts[3]=parseExpr(pciTree.getNode(myPath).getData().decompile())
except :
	print("Could not extract PCI corrected timebase info.")
	#Remove sentinel placeholder values for PCI from data
	t0=t0[0:3]
	ts=ts[0:3]

#Now, write start times and sampling times to saved file
#myDataStr=[ "{0:f}  ".format(num) for num in [t0, ts] ]
myDataStr=''
for num in t0+ts :
	myDataStr=myDataStr+"%(num).15G  " % {"num":num }
#myDataStr=["%(num).15F" % {"num":num } for num in t0+ts] #Plus operation concatenates lists
print(myDataStr)
print(t0)
print(ts)
open(fname,"a+").write(myDataStr)
open(fname,"a+").write("\n")

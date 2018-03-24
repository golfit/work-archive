'''
Created on May 23, 2013

@author: golfit
'''
from MDSplus import *
import pymssql
import re
import sys
import numpy


def parseExpr(myExpr):
    #Get all doubles out of expression
    getNumExpr=re.compile("(-*\d*\.\d+D*-*\d*)")
    dblsAsStrings=getNumExpr.findall(myExpr)
    #Cast strings as floating point numbers
    myNums=[float(re.compile("D").sub("E",myStr)) for myStr in dblsAsStrings]
    t0=myNums[0]
    ts=myNums[1]
    return t0, ts #Return the trigger time and the sampling time

if(len(sys.argv)<2) :
    firstShot=1110307000 #On this day, I made a logbook entry indicating that the timebase synchronization system had been set up on magnetics.
else :
    firstShot=int(sys.argv[1])

if(len(sys.argv)<3) : #If only one shot is specified, retrieve data only for this shot
    sList=[firstShot]
elif(sys.argv[2].lower()=='all') : #All shots are requested, retrieve all shots since the one specified.
    connection=pymssql.connect(host='alcdb2',database='logbook', user='golfit', password='pfcworld')
    cur=connection.cursor()
    cur.execute('select shot from shots where shot>{0:d} order by shot'.format(firstShot))
    ans=cur.fetchall()
    sList=[val[0] for val in ans]

firstShot=sList[0]
lastShot=sList[-1]
indLow=0
indHigh=len(sList)

signalMinVal=0.1 #If signal has a value greater than this, declare that timebase synchronization data exists for this shot

counter=0 #Counter for number of iterations

i=(indHigh-indLow)/2
iLast=-1 
while (i>0 and i<len(sList) and iLast != i and (indHigh-indLow)>1) :
    counter=counter+1
    s=sList[i]

    try :
        pciTree=Tree('pcilocal',s) #Get PCI tree
	#Grab maximum value stored in this channel and test to see if it was high enough to indicate a siganl.
	ymax=Data.execute('maxval(abs(dt216b_1.input_07))')
    except :
	print("No data available for {0:d} - moving to next shot".format(s))
	#Pop shot out of list.
	sList=sList[0:i]+sList[i+1:-1]
	indHigh=indHigh-1 #Adjust upper index down after popping one shot from list.
	i=i+1
	continue

    if( ymax > signalMinVal ) : #Signal data exists for this 
        indLow=i
	print("Data exists for {0:d}".format(s))
    else : #No signal data exists for this shot - limit range of search space accordingly
        indHigh=i

    iLast=i #Store current value of i before changing it
    i=(indHigh+indLow)/2 #Bisect search space

print("Search terminated after {0:d} iterations".format(counter))
print("Shot range from {0:d}-{1:d}".format(firstShot,lastShot))
if(indLow==sList[0]) : #Probably didn't find any shot with signal data - indicate
	print("lower index in search didn't move - probably didn't find shot")
else :
	print("Last shot in range for which there is signal data is {0:d}".format(sList[i]))

print("Lower index={0:d}, upper index={1:d}".format(indLow,indHigh))
print("Lower Shot={0:d}, upper shot={1:d}".format(sList[indLow], sList[indHigh]))
print("i={0:d}, iLast={1:d}".format(i,iLast))


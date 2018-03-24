'''
Created on August 12, 2014
based on processAllFix.py, which, itself, was used to process timebase fix.

Correct ordering mapping of Mirnov coils, BP123T_GHK, to correct digitizer inputs.  Correct mapping at patch panel was lost after coil leads were all ripped during repair during up-to-air prior to 2014 campaign.  See  ChangeBP123CoilInputs12Aug2014.py

@author: golfit
'''
from myTools import getShotRange
import datetime
import sys

sList=getShotRange()

print("Total shot range={0:d}-{1:d}".format(sList[0],sList[-1]))

currentDate=datetime.datetime.now()

startDate=datetime.datetime(2014,8,30,0,0,0) #Start on Saturday, 30 August 2014.

maxShotsPerDay=150

runDays=[5,6] #Days of the week for which code runs, 0=Monday, 6=Sunday

numDaysToFinish=int(len(sList)/maxShotsPerDay) #Cast as int for python3

numDaysElapsed=0

#Count number of run days elapsed
for dayNum in range(0,(currentDate-startDate).days):
    numDaysElapsed+= any([(startDate+datetime.timedelta(dayNum)).weekday()==day for day in runDays])

#Where to start in the list of shots.
startIndex=numDaysElapsed*maxShotsPerDay
endIndex=min(startIndex+maxShotsPerDay-1,len(sList)-1)

if( startIndex>=0 and startIndex<(len(sList)) ) :
    #Run fix - modify sys.argv arguments to make tests work, since these parse sys.argv for shot range
    sys.argv[1]=sList[startIndex]
    sys.argv[2]=sList[endIndex]
    
    subList=getShotRange()
    
    print("Fixing shots {0:d}-{1:d}".format(subList[0], subList[-1]))
    
    execfile("home/golfit/python/versionControlled/trunk/magnetics/ChangeBP123CoilInputs12Aug2014.py")
    
    #Print fixed shot range to log.
    myLogFile=open('Bp123t_ghk2014ChangeLog.txt','a')
    myLogFile.write('{0:s} -> Fixed {1:d}-{2:d}'.format('currentDate',subList[0],subList[-1]))
    myLogFile.close()
    
else :
    print("Can't index into shot list - we may be done with this job already")
    print("Start date was {0:s}".format(str(startDate)))
    print("Current date is {0:s}".format(str(currentDate)))
    print("Difference is {0:s}".format(str(currentDate-startDate)))
    print("Shots processed per day={0:d}".format(maxShotsPerDay))
    print("Exiting program.")

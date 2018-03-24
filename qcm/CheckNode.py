#This script checks the length of an MDSplus signal node to make sure it is larger than a threshold value.
#The idea is that it runs from a scheduled cron task and alerts the user when there is a data system problem.
#
#USAGE:
#
# > python CheckNode.py [node] [userName] [lengthThreshold] [shot]
#
# node = MDSplus node containing signal array to check.  Default = \magnetics::top.
# userEmail = send e-mail to this user if signal array is too short.  Default = golfit@mit.edu
# lengthThreshold = threshold length of signal array (number of data points).  Default = 1000
# shot = shot number.  Default = current shot (as determined from Data.compile('current_shot(cmod)').evaluate() using the MDSplus library).
#
#Ted Golfinopoulos, 31 July 2012

from MDSplus import *
import sys #For getting command line arguments
from myTools import parseList
import numpy
import re
import smtplib
import time
from email.mime.text import MIMEText

#Include myTools module in path
sys.path.append("/home/golfit/python/versionControlled/trunk/qcm/myTools.py")

#Get node if specified by user.
nodeName=[]

if( len(sys.argv)>1 ) :
    nodeName=sys.argv[1]

if(len(nodeName)==0) :
       nodeName='\\magnetics::top.active_mhd.signals.bp1t_ghk'

userEmail=[]
if( len(sys.argv)>2 ) :
    userEmail=sys.argv[2]
else :
    userEmail='golfit@mit.edu'

#Length threshold - signal array must be longer than this, else alert user.
lenThresh=[]
if( len(sys.argv)>3 ) :
    lenThresh=parseList(sys.argv[3])

if(len(lenThresh)==0) :
    lenThresh=1000

sList=[]
if( len(sys.argv)>4 ) :
    sList=parseList(sys.argv[4])

if(len(sList)==0) :
    try :
        sList=[int(Data.compile('current_shot("cmod")').evaluate())]
#        print(sList)
    except :
        time.sleep(60) #Try again after 60 s - if that fails, give up.
        sList=[int(Data.compile('current_shot("cmod")').evaluate())]

def sendEmail(emailAddress,nodeName,s,nodeLength,lenThresh) :
    #Construct message.
    msgStr="Hello - this is an auto-generated message.  Node "+nodeName+" on Shot {0:d} had length, {1:d}, which is less than the specified threshold, {2:d}".format(s, nodeLength,lenThresh)
    print(msgStr)
    msg=MIMEText(msgStr)
    msg['Subject']='AutoMessage: check data for Shot {0:d}'.format(s)
    me=emailAddress
    you=emailAddress
    msg['From']=me
    msg['To']=you

    #Send the message via our own SMTP server; don't include envelope header.
    s=smtplib.SMTP('localhost')
    s.sendmail(me,[you],msg.as_string())
    s.quit()

for s in sList :
    #Parse tree name
    extractTreeName=re.findall('(\\\)(.+)(::)',nodeName)
    if(len(extractTreeName)==0) :
        treeName='magnetics'
    else :
        treeName = extractTreeName[0][1] #Second argument from regular expression output is tree name

    tree=Tree(treeName,s)

    n=tree.getNode(nodeName)

    try :
        y=n.getData().evaluate().data()
    except :
        #Try again after 90 seconds to make sure we didn't just catch this before the store action finished.
        time.sleep(90)
        y=n.getData().evaluate().data()

    #If length of signal array is less than length threshold, alert user.
    if(len(y)<lenThresh) :
        #Try again after 90 seconds to make sure we didn't just catch this before the store action finished.
        time.sleep(90)
        y=n.getData().evaluate().data() #Get data again.
        if(len(y)<lenThresh) : #Still not enough data points in array - alert user.
            sendEmail(userEmail,nodeName,s,len(y),lenThresh)

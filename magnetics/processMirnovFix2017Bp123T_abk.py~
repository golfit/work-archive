#This script compiles several repairs to the Mirnov coils, intended for 2014, 2015, and 2016 campaigns:
#
#1. Add TIMEBASE1, TIMEBASE2, and TIMEBASE3 nodes for 2014 and 2015 campaigns
#       a. In 2014 and 2015, TIMEBASE1 will point to TIMEBASE3
#2. Fix BP1,2,3T_GHK pointers (ACQ_216_1:INPUT_07,08,09)
#3. Turn off BP20_ABK (not actually connected to ACQ_216_3:INPUT_15 - BP28_GHK is) for 2014 and 2015 and 2016 campaigns
#4. Turn off BP28_GHK for 2016 campaign (not actually connected to ACQ_216_3:INPUT_15 = BP26_GHK is)
#5. Turn off BP11_ABK (broken) for 2014 and 2015 and 2016 campaigns
#6. Change digitizer references for BP09,11,12_ABK to ACQ_216_3 (from ACQ_216_2 to ACQ_216_3)
#
#Created on: 28 September 2017, T. Golfinopoulos

from myTools import getShotRange,parseList
import datetime
import sys
import subprocess
from MDSplus import *
import re

#sList=getShotRange(int(sys.argv[1]))
sList=parseList(sys.argv[1])
print(sList)
#Dictionary mapping expression for raw data for corresponding Mirnov coil.  This folds in correct node reference for digitizer, as well as sign.
bp123tghkRawExpr={'bp1t_ghk':'GETNCI(ACTIVE_MHD.SIGNALS.BP1T_GHK, "ON") ? Build_Signal(Build_With_Units(ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_1:INPUT_07 * -1 / (\MAG_RF_COILS:CALIB[59] * 1), "Tesla/s"), *, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE1) : ABORT()',
                'bp2t_ghk':'GETNCI(ACTIVE_MHD.SIGNALS.BP2T_GHK, "ON") ? Build_Signal(Build_With_Units(ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_1:INPUT_08 * 1 / (\MAG_RF_COILS:CALIB[60] * 1), "Tesla/s"), *, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE1) : ABORT()',
                'bp3t_ghk':'GETNCI(ACTIVE_MHD.SIGNALS.BP3T_GHK, "ON") ? Build_Signal(Build_With_Units(ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_1:INPUT_09 * 1 / (\MAG_RF_COILS:CALIB[61] * 1), "Tesla/s"), *, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE1) : ABORT()' }

fixAbkNodes=['bp09_abk','bp11_abk','bp12_abk']

#refFixes2016TopNodes={'bp17_abk':'GETNCI(ACTIVE_MHD.SIGNALS.BP17_ABK, "ON") ? Build_Signal(Build_With_Units(ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3:INPUT_10 * 1 / (\MAG_RF_COILS:CALIB[16] * 1), "Tesla/s"), *, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE3) : ABORT()',
#    'bp20_ghk':'GETNCI(ACTIVE_MHD.SIGNALS.BP20_GHK, "ON") ? Build_Signal(Build_With_Units(ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3:INPUT_14 * 1 / (\MAG_RF_COILS:CALIB[49] * 1), "Tesla/s"), *, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE3) : ABORT()'}

refFixes2016RawExpr={'bp17_abk':'GETNCI(ACTIVE_MHD.SIGNALS.BP17_ABK, "ON") ? Build_Signal(Build_With_Units(ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3:INPUT_10 * 1 / (\MAG_RF_COILS:CALIB[16] * 1), "Tesla/s"), *, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE3) : ABORT()',
                'bp20_ghk':'GETNCI(ACTIVE_MHD.SIGNALS.BP20_GHK, "ON") ? Build_Signal(Build_With_Units(ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3:INPUT_14 * 1 / (\MAG_RF_COILS:CALIB[49] * 1), "Tesla/s"), *, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE3) : ABORT()',
                'bp26_ghk':'GETNCI(ACTIVE_MHD.SIGNALS.BP26_GHK, "ON") ? Build_Signal(Build_With_Units(ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3:INPUT_15 * 1 / (\MAG_RF_COILS:CALIB[55] * 1), "Tesla/s"), *, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE1) : ABORT()'}

#Turn off BP11_ABK, which seems to have been dead (after correcting digitizer reference)
#and BP20_ABK, which seems to have been disconnected starting in 2014 campaign, and sometimes in/out in 2012
#BP1T_ABK looks weak in 2016, as does BP2T_GHK....
turnOffTheseNodes=['bp20_abk','bp11_abk','bp08_ghk','bp4t_ghk']
#GETNCI(.ACTIVE_MHD.SIGNALS:BP09_ABK, "ON") ? Build_Signal(Build_With_Units(.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3:INPUT_09 * -1 / (\MAG_RF_COILS:CALIB[8] * 1), "Tesla/s"), *, .ACTIVE_MHD.SIGNALS:TIMEBASE) : ABORT()



setPosSignNodes=['bp12_abk']
#GETNCI(.-:BP09_ABK, "ON") ? Build_Signal(Build_With_Units(.-.-.DATA_ACQ.CPCI:ACQ_216_3:INPUT_09 * -1 / (\MAG_RF_COILS:CALIB[8] * 1), "Tesla/s"), *, .-:TIMEBASE) : ABORT()
for s in sList :
    #Create calibration structure for each coil and update calibration
    print("Setup Mirnov calibration nodes")
    subprocess.call(["python","SetupMirnovCalibrationNodes.py",str(s)])
    print("Update Mirnov calibration nodes")
    subprocess.call(["python","UpdateMirnovCalibrationNodes.py",str(s)])
    
    recalibrateFlag=False

    #Open tree after calling external Python processes, as connections
    #can get broken.
    myTree=Tree('magnetics',s)
   
    ###
    #Fix BP09,11,12_ABK pointers - swap from ACQ_216_2 to ACQ_216_3.  Do so for raw node,
    #and point top signal node to raw node if it does not point to calibrated node.
    print("Fix BP09,11,12_ABK pointers...")
    for n_name in fixAbkNodes:
        n=myTree.getNode('active_mhd.signals.'+n_name)
        rawNode=n.getNode('raw')
        print(rawNode.getFullPath())
        #print(Data.compile(str(rawNode.getData()).replace('ACQ_216_2','ACQ_216_3')))
        #rawNode.putData(Data.compile(str(rawNode.getData()).replace('ACQ_216_2','ACQ_216_3'))) #This calling sequence was broken by an "improvement" to MDSplus around 6 Oct. 2017
        rawNode.putData(myTree.tdiCompile(str(rawNode.getData()).replace('ACQ_216_2','ACQ_216_3')))
        #If the node data contains a digitizer reference, point to raw node.
        if not re.search('acq_216',str(n.getData()).lower()) is None:
            #n.putData(Data.compile(str(n.getNode('raw').getFullPath()))) #This calling sequence was broken by an "improvement" to MDSplus around 6 Oct. 2017
            n.putData(myTree.tdiCompile(str(n.getNode('raw').getFullPath())))
        #If the node data points to calibration node, re-run calibration,
        #as node was already calibrated, and need to re-calibrate given changes
        if not re.search('calib',str(n.getData()).lower()) is None :
            recalibrateFlag=True
    print("...done")
    ###
    
    ###
    #Fix BP1,2,3T_GHK pointers (ACQ_216_1:INPUT_07,08,09).  Do so for raw node,
    #and point top signal node to raw node if it does not point to calibrated node.
    print('Fix bp123t_ghk...')
    for n_name in bp123tghkRawExpr.keys():
        n=myTree.getNode('active_mhd.signals.'+n_name)
        #print(bp123tghkRawExpr[n_name])
        #n.getNode('raw').putData(Data.compile(bp123tghkRawExpr[n_name])) #This calling sequence was broken by an "improvement" to MDSplus around 6 Oct. 2017
        n.getNode('raw').putData(myTree.tdiCompile(bp123tghkRawExpr[n_name]))
        #print(str(n.getData()).lower())
        #If the node data contains a digitizer reference, point to raw node.
        if not re.search('acq_216',str(n.getData()).lower()) is None:
            #n.putData(Data.compile(str(n.getNode('raw').getFullPath()))) #This calling sequence was broken by an "improvement" to MDSplus around 6 Oct. 2017
            n.putData(myTree.tdiCompile(str(n.getNode('raw').getFullPath())))
        #If the node data points to calibration node, re-run calibration,
        #as node was already calibrated, and need to re-calibrate given changes
        if not re.search('calib',str(n.getData()).lower()) is None :
            recalibrateFlag=True
    print('...done')
    ###
    
    #Open tree after calling external Python processes, as connections
    #can get broken.
    #After ~7:00 PM on 9 Oct., I'm getting errors that the tree is not currently open, even though it manifestly is....-TG
    myTree=Tree('magnetics',s)
    
    ###
    #Correct raw path to BP17_ABK, which had been pointing to a deprecated digitizer node.
    #BP26_GHK, which had been pointing to an input later used for timing input
    if s>=1151204000 : #1151204000=Shot when BP17_ABK had been added
        print('Fix additional refs pointing to wrong digitizer channels for 2016 campaign...')
        for n_name in refFixes2016RawExpr.keys():
            n=myTree.getNode('active_mhd.signals.'+n_name)
            n.getNode('raw').putData(myTree.tdiCompile(refFixes2016RawExpr[n_name]))
            #If the node data contains a digitizer reference, point to raw node.
            if not re.search('acq_216',str(n.getData()).lower()) is None:
                n.putData(myTree.tdiCompile(str(n.getNode('raw').getFullPath())))
        print('...done')
    ###

    
    ###
    #Change sign of nodes with apparently-inverted factors
    print('Set signs to positive value for affected coils...')
    for n_name in setPosSignNodes:
        n=myTree.getNode('active_mhd.signals.'+n_name)
        #n.putData(Data.compile(str(n.getData()).replace('-1','1'))) #This calling sequence was broken by an "improvement" to MDSplus around 6 Oct. 2017
        n.putData(myTree.tdiCompile(str(n.getData()).replace('-1','1')))
        rawNode=n.getNode('raw')
        #rawNode.putData(Data.compile(str(rawNode.getData()).replace('-1','1')))#This calling sequence was broken by an "improvement" to MDSplus around 6 Oct. 2017
        rawNode.putData(myTree.tdiCompile(str(rawNode.getData()).replace('-1','1')))
    print('...done')
    ###
    
    ###
    #Turn off dead/unused channels
    print('Turn off dead/unused coils...')
    if s>=1140000000 :
        for n_name in turnOffTheseNodes:
            n=myTree.getNode('active_mhd.signals.'+n_name)
            n.setOn(False) #Turn off node

    if s>=1160000000 :
        #Turn off BP28_GHK for 2016, since it seems that BP26_GHK is actually in this channel.
        #Similarly, turn off BP20_GHK for 2016, since BP20_GHK is actually in this channel.
        myTree.getNode('active_mhd.signals.bp28_ghk').setOn(False)
        myTree.getNode('active_mhd.signals.bp25_ghk').setOn(False)
        myTree.getNode('active_mhd.signals.bp_ka_bot').setOn(False)
        myTree.getNode('active_mhd.signals.bp_ka_top').setOn(False)
        myTree.getNode('active_mhd.signals.bp_gh_bot').setOn(False)
        myTree.getNode('active_mhd.signals.bp_gh_top').setOn(False)
    print('...done')
    ###
    
    #Add timebase123 nodes for 2014 and 2015 campaigns
    print('Add timebase nodes...')
    if(s>1140000000 and s<1160000000): 
        #Call script to add nodes, passing current shot as shell argument
        subprocess.call(["python","/home/golfit/python/versionControlled/trunk/timebase/createMasterMagTimebaseNode.py",str(s)])
        #Point signals to correct timebase node (after all other corrections made.
        subprocess.call(["python","/home/golfit/python/versionControlled/trunk/timebase/pointMagSignalsToTimebaseNodes.py",str(s)])
    print('...done')
    
    ###
    #If need to recalibrate because data has changed for coils with existing calibration, do so.
    recalibrateFlag=True
    if recalibrateFlag :
        print('Re-run calibration...')
        #subprocess.call(["python","calibrate_mirnov_coils.py",str(s)])
        subprocess.call(["python","calibrate_bp123t_abk.py",str(s)])
        print('...done')
    ###

    print('Done fixing '+str(s))
    print('===================================================')

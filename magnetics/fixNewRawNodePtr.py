from MDSplus import *
import sys
import myTools_no_sql as myTools

sList=myTools.parseList(sys.argv[1]) #0th argument is script name; first argument is shot number.  Parse integer.

#sList=[int(sys.argv[1])]
for s in sList :
    #These two nodes had pointers to non-existent digitizers.  Fix reference to correct digitizer inputs.
    #Need to do this for all of campaign up to and including 1160520
    myTree=Tree('magnetics',s)
    myTree.getNode('\MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:BP17_ABK:RAW').putData(Data.compile('GETNCI( \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:BP17_ABK, "ON") ? Build_Signal(Build_With_Units( \MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3:INPUT_10 * 1 / (\MAG_RF_COILS:CALIB[16] * 1), "Tesla/s"), *, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE3 ) : ABORT()'))
    
    myTree.getNode('\MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:BP20_GHK:RAW').putData(Data.compile('GETNCI( \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:BP20_GHK, "ON") ? Build_Signal(Build_With_Units( \MAGNETICS::TOP.ACTIVE_MHD.DATA_ACQ.CPCI:ACQ_216_3:INPUT_14 * 1 / (\MAG_RF_COILS:CALIB[49] * 1), "Tesla/s"), *, \MAGNETICS::TOP.ACTIVE_MHD.SIGNALS:TIMEBASE3 ) : ABORT()'))
    print("Fixed BP17_ABK:RAW and BP20_GHK:RAW for "+str(s))

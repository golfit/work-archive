from MDSplus import Tree
import sys
limits=[[-10.775885,10.632514],
        [-10.841410,10.729164],
        [-10.515574,10.401434],
        [-10.618536,10.632407],
        [-10.767994,10.615872],
        [-10.780648,10.789758],
        [-10.633335,10.595271],
        [-11.007920,10.958671],
        [-10.716168,10.600871],
        [-10.757820,10.753945],
        [-10.528884,10.418159],
        [-10.687237,10.582137],
        [-10.589798,10.680742],
        [-10.973911,10.871290],
        [-10.334272,10.356784],
        [-10.796816,10.618926]]
t=Tree('magnetics',int(sys.argv[1]))
for i in range(16):
  node=t.getNode('.active_mhd.data_acq.cpci.acq_216_1.input_%02d'%(i+1,))
  try:
    sig=node.record
  except:
    sig=None
  if sig is not None:
    sig.value[0]=limits[i][1]
    sig.value[1][0][0][0]=limits[i][0]
    sig.value[1][0][0][1]=limits[i][1]
    try:
      node.write_once=False
      node.record=sig
      node.write_once=True
    except Exception,e:
      print "Error fixing node %s, error was: %s" % (str(node),str(e))


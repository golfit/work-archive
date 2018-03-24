#This script reads the transfer function from the plunging magnetic probe, fits an exponential to the data, and backs out a decay constant, k_r.  We have k_r \approx k_\perp after assuming that \vec{k}\cdot\vec{B}=0 (field-aligned perturbation) (\cite[p. L28]{Snipes2001}).
#Ted Golfinopoulos, 22 June 2012

from MDSplus import *
from numpy import polyfit
from numpy import log
from numpy import linspace
from numpy import logical_and as logAnd
from numpy import mean
from numpy import array
from scipy.interpolate import interp1d
import myTools
import re
import sys

#Parse shot information, contained in first command-line argument
sList=myTools.parseList(sys.argv[1])

#Time before and after a plunge in which data is considered for radial decay. [s]
DeltaT=0.05

for s in sList :
	print("...Processing radial decay rate for Shot {0:d}".format(s))
	magTree=Tree('magnetics',s,'edit') #Edit to add nodes for fit parameters.
	edgeTree=Tree('edge',s)
	analysisTree=Tree('analysis',s)

	#Grab all nodes with plunging probe data
	allTransNodes=magTree.getNode('shoelace.trans_fun').getNodeWild('*')
	allProbeNodes=[allTransNodes[ii] for ii in myTools.find([re.search(".*BDOT.*",str(x.getPath()))!=None for x in allTransNodes])]

	try :
		rho, tRho = myTools.getYX(edgeTree.getNode('PROBES.ASP.MAG:RHO'))
		#There was a problem with some of the timebases - the number of data points was more than the number of timebase points
		tRho=linspace(tRho[0],tRho[-1],len(rho))

	except :
		print("Could not get radial position data for scanning probes for Shot {0:d}- skipping".format(s))
		continue

	#Get plunge times from Edge tree.
	tPlunge=[ myNode.getData().evaluate().data() for myNode in edgeTree.getNode('probes.asp').getNodeWild('time*')]

	for n in allProbeNodes :
		#Get Hilbert transform data for each probe.
		H,tH=myTools.getYX(n)

		#Fit a first-order polynomial for each plunge time
		kr=[] #Initialize variable to hold radial decay lengths
		q95Plunge=[] #Vector to hold q95
		for tP in tPlunge :
			if(tP==0.) : #A plunge time=0 implies that the probe didn't actually fire - skip
				continue

			rhoPlunge=rho[logAnd(tRho>(tP-DeltaT), tRho<(tP+DeltaT))]
			timePlunge=tRho[logAnd(tRho>(tP-DeltaT), tRho<(tP+DeltaT))]

			#Only fit data for rho within 5 cm of separatrix.
			timePlunge=timePlunge[rhoPlunge<0.05] #Make sure you modify the timebase, first!
			rhoPlunge = rhoPlunge[rhoPlunge<0.05]

			HInterpObj=interp1d(tH, H)
			HPlunge=HInterpObj(timePlunge)

			#Fit a first-order polynomial to the logarithm of the dependent variable given the (linear) dependent data.
			coeffs=polyfit(rhoPlunge,log(abs(HPlunge)),1)
			kr.append(coeffs[0]) #First coefficient is the radial decay constant
			print("...kr={0:f} 1/cm".format(coeffs[0]/100.))

			q95,tq95=myTools.getYX(analysisTree.getNode('\ANALYSIS::TOP:EFIT.RESULTS.A_EQDSK:Q95'))
			q95Mean=mean( q95[logAnd(tq95>timePlunge[0],tq95<timePlunge[-1])] )
			q95Plunge.append(q95Mean)

			#\ELECTRONS::TOP.TCI.RESULTS:NL_04
			#\ANALYSIS::TOP:EFIT.RESULTS.A_EQDSK:Q95
			#\ANALYSIS::EFIT_AEQDSK:QPSIB

		try :
			n.addNode('kr', 'signal')
			magTree.write()
		except :
			#Node may exist already.
			print("Node for decay rate may exist already")

		try :
			n.addNode('q95', 'signal')
			magTree.write()
		except :
			#Node may exist already.
			print("Node for q95 may exist already")

		try :
			n.addNode('comment','text')
			n.getNode('comment').putData('kr = radial decay rate [1/m]; q95=q95 for given plunge time, averaged over time when probe is within 5 cm of separatrix')
		except :
			print("Comment node might already exist.")

		#Save in tree.  Wrap in a numpy array - had problems extracting data without doing this, even though could see no problem in expression.
		n.getNode('kr').putData(Data.compile("BUILD_SIGNAL(real($VALUE),$1,$2)", array(kr), array(tPlunge)))
		n.getNode('q95').putData(Data.compile("BUILD_SIGNAL(real($VALUE),$1,$2)", array(q95Plunge), array(tPlunge)))

		print("Finished calculating radial decay rate for "+n.getPath())

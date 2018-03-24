from numpy import *

#This script calculates some vacuum field approximations to estimate the parallel current driven by the antenna
mu0=4.0E-7*pi

kperp=150 #Perpendicular wave number, m^-1
wmode=0.002 #Width of mode layer, m
Ia=80.0 #Current running through antenna [A]
Nlayers = 2 #Number of layers of antenna winding
Ieff = Ia*Nlayers #Effective current from antenna windings on meandering pattern [A]

DeltaX=[0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.010]

for i in range(0,len(DeltaX)) :
	Hy=Ieff*kperp/(2.0*pi)/sinh(kperp*DeltaX[i])
	By=mu0*Hy
	Jpar=Hy/wmode
	print("DeltaX="+str(DeltaX[i])+" and kperp*DeltaX="+str(kperp*DeltaX[i]))
	print("Hy="+str(Hy))
	print("By="+str(By))
	print("Jpar="+str(Jpar))


'''
This script is meant to estimate the component contributions to the fluctuation free energy of the QCM using 1120814028 as a base shot and data from the A-port Scanning Probe with the mirror system.

Ted Golfinopoulos, 28 Nov 2012
'''

#Import packages
from numpy import *

#Load constants
execfile('constants.py')

#Declare parameters
timeSlice=1.1964; #Time data is analyzed in LaBombard2014 PoP for 11208014028
Tebar=q_e*50.E0 #Electron temperature, kB*temp
#nebar=1.5E20 #Approximate average density at time where fluctuation amplitudes are taken, [m^-3].
nebar=1.0E20;
B0=2.8905# From 1120814028 #3 T is from 1120814021; #4 #Magnetic field at mag. axis, (approximate) [T]
R0=0.68 #Approximate major radius of magnetic axis, [m]
rsep=0.22 #Approximate minor radius of separatrix where probe is launched, [m]
#B=B0*R0/(R0+rsep)
#B=2.2489 #This corresponds to the total B field (magnitude of all components) at the position of the MLP at 1.1964 s on 1120814028.
B=2.27
q95=3 #Approximate q95

kperp=150 #perpendicular wave number, m^-1
f0=100E3 #Fluctuation frequency, [kHz]
omega=2*pi*f0
m=kperp*rsep #Poloidal mode number
n=m/q95 #Toroidal mode number - assume mode is field-aligned.
Lc=9 #Connection length [m] - length connecting point near x-pt to top of plasma on bad-curvature side and on LCFS
#kpar=n/(R0+rsep)
kpar = pi/Lc #Approximate parallel wavelength to be twice the connection length.
Mi=2.01410178*amu #Mass of ions (deuterons)

Lp=3.6E-3 #Pressure gradient scale length, m. - Formerly in calculations 3.E-3 m - 3.6 mm is based on ASP fit for North, South, and West probes from rho=-0.007425 to -0.005121 m on 1120814028.

OmegaI=q_e*B/Mi #ion cyclotron frequency
cs=sqrt(Tebar/Mi) #Sound speed
rhos=cs/OmegaI #drift dispersion scale

#Fluctuation amplitudes at or near mode layer - approximate!  Roughly taken at 1.195 s
phi=15  #Electrostatic potential, [V] #I had phi=150 before, but this was wrong, it appears.
Te=Tebar/3 #kB*Temperature, [J] - originally, 60*q_e
pebar=nebar*Tebar #Average electron pressure, [Pa]
ne=nebar; #Approximate density [m^-3]   1.5E20 #time-averaged electron density at the LCFS on 1120814021, [m^-3]
pe=5000/3 #Pressure fluctuation, [Pa]
Bp=1E-4 #Perpendicular (poloidal) magnetic field fluctuation - not taken from data!  Approximate.  [T]
Apar=Bp/kperp #Parallel vector magnetic potential fluctuation component, [T.m]

betae=pebar*mu0/pow(B,2) #Dynamical beta.

lambdaDebye=sqrt(epsilon0*Tebar/(pow(q_e,2)*nebar)) #Debye length [m]
Lambda=4*pi/3*nebar*pow(lambdaDebye,3) 
#Electron and ion collision times - P. 29 of Mag. Fus. Formulary
tau_ei=12.0*sqrt(pow(pi,3)*pow(epsilon0,4)*m_e*pow(Tebar,3))/(sqrt(2)*nebar*pow(q_e,4)*log(Lambda))
tau_ii=12.0*sqrt(pow(pi,3)*pow(epsilon0,4)*Mi*pow(Tebar,3))/(sqrt(2)*nebar*pow(q_e,4)*log(Lambda))

nue=0.51/tau_ei #0.51 factor is for Spitzer
#nue=0.51*sqrt(2)*nebar*pow(q_e,4)*log(Lambda)/(12*pow(pi,3./2.)*pow(epsilon0,2)*sqrt(m_e)*pow(Tebar,3./2)) #Collisionality (electrons), 1/s

#2\frac{k_{\perp}^2}{k_{\parallel}^2}\frac{\omega_{pi}^2}{\Omega_{ci}^2}\frac{\omega^2}{\omega_{pe}^2}

print nue/(omega)

#Calculate component contributions to fluctuation free energy
#Thermal energy
Ut=3*pe #Assuming pe=pi
vthe=sqrt(2*Tebar/m_e) #Really assuming vthe=vthe,|| and Tebar=Tebar,||, so that (1/2)*m_e*v_{the,||} = T_{ebar,||}
print("Ut={0:e} J/m^3".format(Ut))

#Kinetic energy
vdiamag=cs*rhos/Lp
vexb=kperp*phi/B
valfven=B/sqrt(nebar*Mi*mu0)
omegaStar=vdiamag*kperp
Ukexb=(0.5)*nebar*Mi*pow(vexb,2)
Ukdiamag=(0.5)*nebar*Mi*pow(vdiamag,2)
Uk=Ukexb+Ukdiamag #Don't know contribution from parallel velocity - don't have this fluctuation amp.
print("ExB Velocity={0:e} km/s".format(vexb/1.E3))
print("Electron Diamag. Velocity={0:e} km/s".format(vdiamag/1.E3))
print("Sound Speed = {0:f} km/s".format(cs/1.E3))
print("Diamag. Freq. = {0:f} kHz".format(omegaStar/(2*pi*1000.0)))
print("Drift dispersion scale=rho_s={0:e} m".format(rhos))
print("Uk_exb={0:e} J/m^3".format(Ukexb))
print("Uk_diamag={0:e} J/m^3".format(Ukdiamag))
print("Uk_total={0:e} J/m^3".format(Uk))

#Electromagnetic energy
UemEfield=(epsilon0/2)*(pow(kperp*phi,2)+pow(omega*Apar+kpar*phi,2))
UemJustApar=(epsilon0/2)*(pow(omega*Apar,2))
UemBfield=pow(kperp*Apar,2)/(2*mu0)
Uem=UemEfield+UemBfield
print("Uem_Apar={0:e} J/m^3".format(UemJustApar))
print("Uem_Efield={0:e} J/m^3".format(UemEfield)) #Largest contribution to electric field stored energy is from electrostatic components
print("Uem_Bfield={0:e} J/m^3".format(UemBfield))
print("Uem_total={0:e} J/m^3".format(Uem))

#Results in
#Ut=4.998000e+03 J/m^3
#Uk_exb=1.150459e+01 J/m^3
#Uk_diamag=3.538327e+00 J/m^3
#Uk_total=1.504292e+01 J/m^3
#Uem_Apar=7.767763e-13 J/m^3
#Uem_Efield=2.256103e-03 J/m^3
#Uem_Bfield=3.978874e-03 J/m^3
#Uem_total=6.234977e-03 J/m^3

#More calculations for Scott normalization.
#Lperp=2*pi/kperp #I think this is very wrong.
Lperp=Lp

tau=Lperp/cs #Time scale

#Lpar=2*pi*(R0+rsep)/2*q95/2 #Take parallel length scale to be the path travelled by a field line on the 95% flux surface on the outer half poloidal circuit.
Lpar=Lc
kpar=pi/Lpar
omegap=Lperp/Lp
epsilon=pow(Lpar/(2.*pi*Lperp),2)
betaHat=betae*epsilon
kperpHat=kperp*rhos #Perpendicular gradient is normalized to rhos when acting on a dependent variable.
kparHat=1 #Parallel gradient is normalized to parallel wave number.

omegaHat=omega*tau #Normalized mode frequency.

mue=m_e/Mi #Electron/ion mass ratio.

muHat=mue*epsilon

nuHat=nue*tau

print("nebar="+str(nebar)+" m^-3")
print("Tebar="+str(Tebar/q_e)+" eV")
print("B="+str(B)+" T")
print("kpar="+str(kpar)+" m^-1")
print("kperp="+str(kperp)+" m^-1")
print("Lp="+str(Lp)+" m (pressure gradient length scale)")
print("rho_s="+str(rhos)+" m")
print("cs="+str(cs)+" m/s")
print("tau=Lperp/cs="+str(tau)+" s")
print("nu_ei=0.51/tau_ei="+str(nue)+" s")
print("Omega_i=2*pi*"+str(Wc/(2*pi))+" Hz")
print("beta_e="+str(betae))

print("omega_p="+str(omegap))
print("epsilon="+str(epsilon))
print("betaHat="+str(betaHat))
print("kperpHat="+str(kperpHat))
print("kparHat="+str(kparHat))
print("mu_e = m_e/M_i = "+str(mue))
print("muHat=mue*epsilon="+str(muHat))
print("nuHat=nu_ei*tau="+str(nuHat))

C0=-1j*omegap*pow(kparHat,2)/kperpHat
C1=pow(kparHat,2)/pow(kperpHat,2)
C2=-(1j*omegap*betaHat/kperpHat+0.51*muHat*nuHat)
C3=betaHat/pow(kperpHat,2)

s0=-C0/C1
gammaHat=-0.51*muHat*nuHat*pow(kperpHat,2)*pow(imag(s0),2)
sr1=-(C2/(2.0*C3))+1j*sqrt(C1/C3)
sr2=-(C2/(2.0*C3))-1j*sqrt(C1/C3)


myRoots=roots([C3,C2,C1,C0])

print("C0:="+str(real(C0))+"+I*"+str(imag(C0))+";")
print("C1:="+str(real(C1))+"+I*"+str(imag(C1))+";")
print("C2:="+str(real(C2))+"+I*"+str(imag(C2))+";")
print("C3:="+str(real(C3))+"+I*"+str(imag(C3))+";")

print("rho_s="+str(rhos)+" m")
#print("rho_s={0:d} m".format(rhos))

print("Exact roots=")
print(myRoots)

print("Approximate Roots=")
print("s0="+str(s0)+"+"+str(gammaHat))
print("s1="+str(real(sr1))+"+i"+str(imag(sr1)))
print("s2="+str(real(sr2))+"+i"+str(imag(sr2)))

print("In real units")

print("Exact roots [kHz]")
print(myRoots/tau/(2*pi*1E3))

print("Approximate Roots [kHz]")
print("s0="+str(s0/(tau*2*pi*1E3))+"+"+str(gammaHat/(tau*2*pi*1E3)))
print("s1="+str(real(sr1)/(tau*2*pi*1E3))+"+i"+str(imag(sr1)/(tau*2*pi*1E3)))
print("s2="+str(real(sr2)/(tau*2*pi*1E3))+"+i"+str(imag(sr2)/(tau*2*pi*1E3)))

### Kuehl1974 - model for resonance cone for omega<<Omega_c
#Look at what happens when reverse direction of kpar
kpar=2 #-pi/Lc
w=omega
wp=sqrt(ne*pow(q_e,2)/(epsilon0*m_e)) #Electron plasma frequency [rad/s]
wc=q_e*B/m_e #Electron cyclotron frequency [rad/s]
Wp=sqrt(ne*pow(q_e,2)/(epsilon0*Mi)) #Ion plasma frequency [rad/s]
Wc=q_e*B/Mi #Ion cyclotron frequency [rad/s]

vthe=sqrt(2.0*Tebar/m_e) #Electron thermal velocity [m/s]
Vthi=sqrt(2.0*Tebar/Mi) #Ion thermal velocity ASSUMING Ti=Te [m/s]

RLi=Vthi/(sqrt(2)*Wc) #Ion Larmour radius [m] - See Kuehl1974 - factor of 2 in there
rLe=vthe/(sqrt(2)*wc) #Electron Larmour radius [m] - See Kuehl1974 - factor of 2 in there
zeta_e0=w/(kpar*vthe) #Argument to plasma dispersion function, See Stix "Waves in Plasmas" Chapter 8, Eq. 81, 82 on P. 202, etc.

lambdaZ=1j*sqrt(pi) #See P. 204 in Stix "Waves in Plasmas"
Sfun=zeta_e0-2.0*pow(zeta_e0,3)/3.0 + 2.0*2.0*pow(zeta_e0,5)/(5*3*1) - 2*2*2*pow(zeta_e0,7)/(7*5*3*1)+2*2*2*2*pow(zeta_e0,9)/(9*7*5*3*1) #Assymptotic expansion of S - Eq. 8.88 in Stix "Waves in Plasmas" on Page 204
Zfun=-2.0*Sfun+lambdaZ*exp(-pow(zeta_e0,2))
Zp=-2*(1+zeta_e0*Zfun) #dZ(zeta)/dzeta (See Eq. 8.86 on Page 204 on Stix "Waves in Plasmas")
#

#Dispersion relation parameters
AA=3.0*pow(Wp,2)*pow(Wc,2)/((w*w-Wc*Wc)*(4.0*Wc*Wc-w*w))

BB=1-Wp*Wp/(w*w-Wc*Wc)-pow(wp,2)/pow(wc,2)*(zeta_e0*Zp) - pow(Wp*Wc,2)*( 6*pow(w,4)-3*pow(w*Wc,2)+pow(Wc,4) )/( pow(w,2)*pow(pow(w,2)-pow(Wc,2),3) )*pow(kpar*RLi,2)

CC=pow(kpar*RLi,2)*( 1-pow(wp/w,2)*pow(zeta_e0,2)*Zp-pow(Wp/w,2) - 3.0*pow(Wp*Wc*kpar*RLi/(w*w),2) )

kperp1Squared=-CC/BB/pow(RLi,2)
kperp1=sqrt(kperp1Squared)
#Parallel and perpendicular cold plasma electrostic dielectric constants
KPar=1-pow(wp/w,2)
KPerp=1+pow(wp/wc,2)-pow(Wp,2)/(pow(w,2)-pow(Wc,2))

kperp2Squared=( (pow(Wp/w,2)-1)/KPerp * (pow(kpar,2)-pow(w,2)*Mi/(Tebar*(1-pow(w/Wp,2))))  )+0*1j
kperp2=sqrt(kperp2Squared)
print(kperp1)

#Electron and ion collision times - P. 29 of Mag. Fus. Formulary
tau_ei=12.0*sqrt(pow(pi,3)*pow(epsilon0,4)*m_e*pow(Tebar,3))/(sqrt(2)*nebar*pow(q_e,4)*log(Lambda))
tau_ii=12.0*sqrt(pow(pi,3)*pow(epsilon0,4)*Mi*pow(Tebar,3))/(sqrt(2)*nebar*pow(q_e,4)*log(Lambda))

#Electron and ion collisionalities with zero species mean velocities
#Assume ni=ne, Ti=Te
m_reduced=m_e*Mi/(m_e+Mi)
nu_ei=(1/(1.3*pow(Vthi,3)))*(pow(q_e,4)*nebar*log(Lambda))/(4.0*pi*pow(epsilon0,2)*m_e*m_reduced)
nu_ee=(1/(1.3*pow(vthe,3)))*(pow(q_e,4)*nebar*log(Lambda))/(2.0*pi*pow(epsilon0,2)*m_e*m_e)
nu_ii=(1/(1.3*pow(Vthi,3)))*(pow(q_e,4)*nebar*log(Lambda))/(2.0*pi*pow(epsilon0,2)*m_e*m_e)
nu_ie=(1/(1.3*pow(vthe,3)))*(pow(q_e,4)*nebar*log(Lambda))/(4.0*pi*pow(epsilon0,2)*m_e*Mi)

#Spitzer resistivity
etas = 0.51*m_e/(ne*q_e*q_e*tau_ei)

Lc=9.0 #Connection length [m]
kpar = 2*pi/(2*Lc) 
gamma_ideal = epsilon0 * etas * pow(kperp/kpar,2)* pow(cs/Lp,2)*pow(kperp*cs*Wp/(Wc*Wc),2)


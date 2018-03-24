#Ted Golfinopoulos, 5/1/2007
#From Wikipedia.
#Transposed to Python on 20 Nov 2012
from numpy import pi
hPlank=6.6260693E-34; #Planck's Constant: J.s. #Backwards compatibility for old error.
hPlanck=6.6260693E-34; #Planck's Constant: J.s.
hbar = hPlank*2*pi;
c0 = 2.99792458E8; #Speed of light in vacuum, m/s (exact definition - see Wikipedia).
q_e = 1.60217653E-19; #Fundamental charge, C.
kB = 1.3806505E-23; #Boltzmann constant, J/K, or 
kBeV = 8.617343E-5; #Boltzmann constant in eV/K.
F=96485.3383E0; #Faraday number, coulomb/mol.
R=8.314472E0; #Gas constant, J/mol K.
Na = 6.02214179E23; #Avogadro's number, mole^-1.
m_e = 9.10938215E-31; #Electron mass, kg.
mu0=4E-7*pi; #Permeability of free space.

epsilon0=1.E0/(pow(c0,2)*mu0); #Permittivity of free space.

#Conversion factors from
#http://www.people.cornell.edu/pages/jf262/Conversion_Factors.htm
kcalPerMol2eV=0.04336;
eV2kcalPerMol=23.06;
kcalPerMol2kJPerMol=4.184;

eV2kJPerMol=Na*q_e/(1000.E0); #This is right - leave it.

amu=1.660538782E-27; #kilograms per atomic mass unit. 
atm2Pa=101325.E0; #Number of pascals (Pa) per atmosphere (atm) pressure.

m_H=1.0078250*amu
m_D=2.014102*amu
m_T=3.0160492*amu

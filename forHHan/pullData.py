'''
This script was originally written for Valentin Aslanyan to support his Alfven eigenmode studies using Alcator C-Mod data.  It can now be adapted for Harry Han for his DEGAS2 modeling of GPI conditions, especially regarding how the puff perturbs the edge plasma.

T. Golfinopoulos
v1. 17 Nov. 2017
v2. 17 Mar. 2018
'''
from MDSplus import *
import eqtools #Use toolbase written by Chilenski, Walk, and Faust for pulling and writing out EFIT data
import sys
import numpy
from numpy import zeros, interp, array, ceil, floor, where, squeeze, size
import matplotlib.pyplot as plt
import geqdskio #Import i/o geqdsk tools from Dudson geqdsk.py
from geqdsk_cls import Geqdsk
import scipy.io

#s=int(sys.argv[1]) #Parse shot number from command line argument

#s=1140807015 #GPI shot - look for perturbation from puff
#tPt=0.9 #Puff may not have hit by then

s=1140521012 #Christian Theiler's shot
tPt=1.065


#Pull Thomson profiles
myTree=Tree('electrons',s)
#Core
try :
    tThom=myTree.getNode('yag_new.results.profiles.ne_rz').getDimensionAt(0).data() #Pull timebase
    neThom=myTree.getNode('yag_new.results.profiles.ne_rz').data()
    TeThom=myTree.getNode('yag_new.results.profiles.te_rz').data()
    rhoThom=myTree.getNode('yag_new.results.profiles.rho_t').data()
    RmidThom=myTree.getNode('yag_new.results.profiles.r_mid_t').data()
    coreThomSuccess=True
except :
    coreThomSuccess=False
#Edge
try:
    neThomEdge=myTree.getNode('yag_edgets.results.ne').data()
    TeThomEdge=myTree.getNode('yag_edgets.results.te').data()
    rhoThomEdge=myTree.getNode('yag_edgets.results.rho').data()
    RmidThomEdge=myTree.getNode('yag_edgets.results.rmid').data()
    edgeThomSuccess=True
except :
    edgeThomSuccess=False

def thisInterp(t,y):
    '''
    Syntactic sugar for interpolating profile data at desired time-point.
    Can extend to average over several time points.
    '''
    return numpy.array([interp(tPt,t,u) for u in y])

if(coreThomSuccess) :
    RPt=thisInterp(tThom,RmidThom)
    nePt=thisInterp(tThom,neThom)
    TePt=thisInterp(tThom,TeThom)
    #Print profile data to screen
    print('Core Thomson')
    print('Rmid [m]\tne [m^-3]\tTe [eV]')
    for i in range(len(RPt)):
        print(str(RPt[i])+'\t'+str(nePt[i])+'\t'+str(TePt[i]))
else :
    print("Could not pull core Thomson data for this shot, "+str(s))

if(edgeThomSuccess):
    RPtEdge=thisInterp(tThom,RmidThomEdge)
    nePtEdge=thisInterp(tThom,neThomEdge)
    TePtEdge=thisInterp(tThom,TeThomEdge)

    print('Edge Thomson')
    print('Rmid [m]\tne [m^-3]\tTe [eV]')
    for i in range(len(RPtEdge)):
        print(str(RPtEdge[i])+'\t'+str(nePtEdge[i])+'\t'+str(TePtEdge[i]))
else :
    print("Could not pull edge Thomson data for this shot, "+str(s))

#Plot profile
#plt.grid(color='k', linestyle='-', linewidth=0.5)
#plt.plot(rPt,nePt/1E20,linestyle='',marker='o')
#plt.hold('True')
#plt.plot(rPtEdge,nePtEdge/1E20,linestyle='',marker='o')
#plt.xlabel('R [m]')
#plt.ylabel('$n_e$ [$\\times10^{20} $m$^{-3}$]')
#plt.show()

#Create EFIT object - pull EFIT data from tree
print("Attempting to generate EQDSK file from EFIT tree")
myEq=eqtools.CModEFITTree(s)

#Cache useful EFIT parameters
tEfit=myEq.getTimeBase()
eqInfo=myEq.getInfo()

RGrid=myEq.getRGrid()
zGrid=myEq.getZGrid()
R0=myEq.getMagR() #Major radius of magnetic axis
z0=myEq.getMagZ() #Height of magnetic axis
B0=myEq.getBtVac() #Vacuum toroidal field on axis
psi0=myEq.getFluxAxis()
psiBndry=myEq.getFluxLCFS()
psiRz=-1.0*myEq.getCurrentSign()*myEq.getFluxGrid()
Bcentr=myEq.getBCentr()
Ip=myEq.getIpCalc()
fPol=myEq.getF()
pres=myEq.getFluxPres()
qPsi=myEq.getQProfile()
Rlcfs=myEq.getRLCFS()
zlcfs=myEq.getZLCFS()
Rwall,zwall=myEq.getMachineCrossSection()
tInd=where(abs(tEfit-tPt)==min(abs(tEfit-tPt)))

#Put data into dictionary for writing to geqdsk file
eqDat = {'nx': len(RGrid), 'ny':len(zGrid),        # Number of horizontal and vertical points
          'rdim':max(RGrid)-min(RGrid), 'zdim':max(zGrid)-min(zGrid),         # Size of the domain in meters
          'rcentr':myEq.getRCentr(), 'bcentr':Bcentr[tInd], # Reference vacuum toroidal field (m, T)
          'rgrid1':min(RGrid),                  # R of left side of domain
          'zmid':zGrid[floor(len(zGrid)/2)],                      # Z at the middle of the domain
          'rmagx':R0[tInd], 'zmagx':z0[tInd],     # Location of magnetic axis
          'simagx':psi0[tInd], # Poloidal flux at the axis (Weber / rad)
          'sibdry':psiBndry[tInd], # Poloidal flux at plasma boundary (Weber / rad)
          'cpasma':Ip[tInd], 
          'psi':squeeze(psiRz[tInd,:,:]),    # Poloidal flux in Weber/rad on grid points
          'fpol':squeeze(fPol[tInd,:]),  # Poloidal current function on uniform flux grid
          'pressure':squeeze(pres[tInd,:]),  # Plasma pressure in nt/m^2 on uniform flux grid
          'qpsi':squeeze(qPsi[tInd,:]),  # q values on uniform flux grid
          'nbdry':len(squeeze(Rlcfs[tInd,:])), 'rbdry':squeeze(Rlcfs[tInd,:]), 'zbdry':squeeze(zlcfs[tInd,:]), # Plasma boundary
          'nlim':len(Rwall), 'xlim':Rwall, 'ylim':zwall} # Wall boundary

fname=str(s)+'_'+str(int(round(tPt*1E3)))+'ms.geqdsk'
#Write geqdsk file.
geqdskio.write(fname,eqDat)

#Test geqdsk file - read it back into Python; export to Matlab file and examine there.
#testRead=geqdskio.read(fname)
#g=Geqdsk()

#g.openFile(fname)

#all_data=g.data

#for i in range(len(all_data)):
#    #filename='1170514001geqdsk_t'+str(i)
#    filename='test_geqdsk'+str(i)
#    print(filename)
#    scipy.io.savemat(filename,all_data[i])

#This script tests the cohereSpecgram method in myTools - a cross-coherence spectrogram.
#Ted Golfinopoulos, 15 Aug 2012

from myTools import *
import numpy as np
import matplotlib
from MDSplus import *
from numpy import logical_and as logicAnd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib.mlab
from numpy import absolute as abs
from scipy.signal import convolve2d

import myTools

import pdb

#s=1120814031
s=1120814021
magTree=Tree('magnetics',s)
pciTree=Tree('pcilocal',s)

ia,ti=getYX(magTree.getNode("shoelace.ant_i"))
#y,ty=getYX(pciTree.getNode("results:pci_31"))
y,ty=getYX(magTree.getNode("active_mhd.signals.bp1t_ghk"))

t1=0.5
t2=1.5

#Restrict signals to time range of interest to save computational effort
ia=ia[logicAnd(ti>t1,ti<t2)]
ti=ti[logicAnd(ti>t1,ti<t2)]
y=y[logicAnd(ty>t1,ty<t2)]
ty=ty[logicAnd(ty>t1,ty<t2)]

#Downsample pci signal onto magnetics signal timebase.
interpObj=interp1d(ty,y)
y=interpObj(ti)

nfft=1024
fs=1.0/(ti[1]-ti[0])

#Cxy,f,t=cohereSpecgram(x, y, nfft, fs)
myInds=numpy.logical_and(ti>t1,ti<t2)
Cxy,f,t=myTools.cohereSpecgram(ia[myInds],y,nfft,fs,noverlap=nfft/2,nxavg=6)
#T=T-T[0]+ti[0]

#Pxx,f,t=mlab._spectral_helper(x,x,nfft,fs)
#Pyy,f,t=mlab._spectral_helper(y,y,nfft,fs)
#Pxy,f,t=mlab._spectral_helper(x,y,nfft,fs)

nxavg=6
#wx=np.empty([1,nxavg])
#wx[:]=1./nxavg

nyavg=6
#wy=np.empty([nyavg,1])
#wy[:]=1./nyavg
#w=np.empty([nxavg,nyavg])
#w[:]=1./(nxavg*nyavg)

#w=np.empty([nyavg,nxavg])
#w[:]=1./(nxavg*nyavg)

#Cxy=convolve2d(Pxy,w,'same','symm')**2/(convolve2d(Pxx,w,'same','symm')*convolve2d(Pyy,w,'same','symm'))

#Cxy=convolve2d(convolve2d(Pxy,wx,'same','symm'),wy,'same','symm')**2/(convolve2d(convolve2d(Pxx,wx,'same','symm'),wy,'same','symm')*convolve2d(convolve2d(Pyy,wx,'same','symm'),wy,'same','symm'))
#Cxy=convolve2d(convolve2d(Pxy,wx,'same','symm'),wy,'same','symm')**2/(convolve2d(convolve2d(Pxx,wx,'same','symm'),wy,'same','symm')*convolve2d(convolve2d(Pyy,wx,'same','symm'),wy,'same','symm'))

#myTools.myImshow(t,f/1.E3,abs(Cxy),origin='lower')

plt.imshow(abs(Cxy)**2,origin='lower')
plt.show()

#plt.figimage(abs(Cxy))

#plt.show()

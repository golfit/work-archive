from numpy import *
from calcCenterFreq import *
import matplotlib.pyplot as plt
from MDSplus import *
from myTools import getYX

#Make a signal which changes freqency.  Calculate center frequency with calcCenterFreq.  Verify that it recovers frequency.

fs=1E5 #Sampling frequency.
f0=1E3
f1=2E3
t=linspace(0,1,fs)
f=ones(len(t))*f0
f[t>0.5]=f1

#y=cos(2*pi*f*t)+(random.rand(len(t))-0.5)*0.2
s=1120712029
tree=Tree('pcilocal',s)
y,ty=getYX(tree.getNode('results.pci_07'))
fs=1.0/(ty[1]-ty[0])

[fp,tp]=getFPeak( y, fs, [50.E3, 200.E3], 1024 )

print(fp)
print(tp)

print(size(fp,0))
print(size(tp,0))

print("Min Freq. = {0:f} [Hz]".format(min(fp)))

plt.plot(tp,fp)
plt.show()
#execfile('TestCalcCenterFreq.py')


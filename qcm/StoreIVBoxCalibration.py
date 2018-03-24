#This script stamps frequency-dependent I/V calibrations into tree.  The calibrations take the form of a signal with frequency as the independent axis (the "dimension" in MDSplus parlance) and a complex multiplicative transfer function as the dependent variable.

import sys #For getting command line arguments
from MDSplus import *
from numpy import polyval, real, imag, array

if(len(sys.argv)>1) :
	s=int(sys.argv[1]) #Grab shot number from command line.
else :
	s=-1 #Default to shot -1

nodeList=['ant_v','ant_i','match_v','match_i','src2_v','src2_i','src_v','src_i','spare_v','spare_i','v_pickup']

commentStr="Multiplicative, frequency dependent calibration transfer function, H.  Usage: Y_{calibrated}(f)=H(f) * Y_{raw}(f).  H_real and H_imag are the real and imaginary parts of the calibration factor, and their frequency axis is given in freq_axis (with units of hertz).  The calibration factor is meant to be interpolated linearly across the frequency points."

freq_axis=[0, 1.0E6]

##Box 4: Vref/Vbox = (2.86e-06+j2.99e-07) f + (1.99e+02+j2.43e-01) 
#Polynomial coefficients for transfer functions, with independent variable of polynomial the frequency (in Hz).  [ [slope, y-intercept], [slope, y_intercept],... ]
H_of_f_coeff=[[2.99E-6+1j*4.04e-7, 1.98e2+1j*2.35e-1],\
[0.0, -100.0],\
[2.86e-6+1j*2.99e-7, 1.99e+02+1j*2.43e-01],\
[0.0,100.0],\
[2.10e-06+1j*1.38e-06, 1.98e+02+1j*1.97e-01],\
[0.0,100.0],\
[2.91e-06+1j*1.52e-06, 2.00e+02+1j*1.98e-01],\
[0.0,100.0],\
[3.3775e-06+1j*-2.2067e-06, 2.0008e+02+1j*3.1356e-01],\
[0.0,10.0],\
[0.0,1.0]
]

tree=Tree('magnetics',s)

for ii in range(0,len(nodeList)) :
    topNode=tree.getNode('shoelace.'+nodeList[ii]+".cal_vs_freq")
    this_H=polyval(H_of_f_coeff[ii],freq_axis)
    H_imag=imag(this_H)
    H_real=real(this_H)
    #Stamp signal expression in top node that pulls data from sub nodes.
    topNode.putData(Data.compile("Build_Signal(Cmplx("+str(topNode)+".H_real,"+str(topNode)+".H_imag), *, "+str(topNode)+".freq_axis)"))
    #Stamp data into node
    topNode.getNode("H_imag").putData(Data.compile("$1",H_imag))
    topNode.getNode("H_real").putData(Data.compile("$1",H_real))
    topNode.getNode("freq_axis").putData(Data.compile("$1",numpy.array(freq_axis))) #Apparently, putData wants numpy arrays - a data type conflict exception is raised on regular array of floating point numbers
    topNode.getNode("comment").putData(commentStr)
    
    print("Finished adding data into "+str(topNode))
#    print("H_imag="+str(H_imag))
#    print("H_real="+str(H_real))
#    print("freq axis="+str(freq_axis))
    
print("Done updating calibration for Shot #"+str(s))

#    Build_Signal(Build_With_Units(F_CLK*M/("+datPath+"), \"Hz\"), *, DIM_OF("+datPath+") )

#VOLTAGE CALIBRATIONS - SEE LOGBOOK ENTRY FROM 11401006XXX
#Box 1: Vref/Vbox = (2.91e-06+j1.52e-06) f + (2.00e+02+j1.98e-01)
#Box 2: Vref/Vbox = (2.10e-06+j1.38e-06) f + (1.98e+02+j1.97e-01)
#Box 3: Vref/Vbox = (2.99e-06+j4.04e-07) f + (1.98e+02+j2.35e-01)
#Box 4: Vref/Vbox = (2.86e-06+j2.99e-07) f + (1.99e+02+j2.43e-01) 
#Spare: Vref/Vbox = (3.3775e-06+i-2.2067e-06)f+(2.0008e+02+i3.1356e-01) 

#Allocation of I/V Boxes:
#I/V Box #3: Antenna position (i.e. looking into antenna)
#I/V Box #4: Match position (i.e. looking into matching network, at output from transformers)
#I/V Box #2: Output from Amplifier #2
#I/V Box #1: Output from Amplifier #1 


#expr=Data.compile("Cmplx("+n.getNode('Cxy_r').getPath()+","+n.getNode('Cxy_i').getPath()+")")
#		n.putData(expr)



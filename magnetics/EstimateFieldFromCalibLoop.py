'''
This script estimates the field pattern for the dipole loop used to calibrate the Mirnov coils.

Ted Golfinopoulos, 4 August 2015
'''

import numpy
from numpy import cos, sin, pi, sqrt, angle, hypot, linspace, meshgrid, zeros, real, imag
from scipy.integrate import quad, ode
from matplotlib.pyplot import plot, figure

R=0.8 #Radius of coil [m]
I=1.0 #Current of coil [A]
mu0=4.0E-7*pi #Permeability of free space [H/m]

#Coordinates are zbar and xbar - these are the major radial and vertical coordinates, normalized by R.

def denom( theta, xbar, zbar) :
    return pow(xbar**2 - 2.0*xbar*cos(theta)+1+zbar**2,3.0/2.0)

def z_comp( theta, xbar, zbar ) :
    val=(1.0-xbar*cos(theta)) / denom(theta,xbar,zbar)
    return real(val)

def r_comp( theta, xbar, zbar ) :
    #print("xbar="+str(xbar)+", zbar="+str(zbar)) #Test
    return real((zbar*cos(theta))/denom(theta,xbar,zbar))

def getField( xbar, zbar ) :
    if(zbar==0.0) :
        BR=0.0
        Rerr=0.0
    else :
        BR,Rerr=quad(r_comp,0,2.0*pi,args=(xbar,zbar))
    Bz,Zerr=quad(z_comp,0,2.0*pi,args=(xbar,zbar))
    scale_val=-mu0*I/(4*pi*R)
    return (scale_val*BR,scale_val*Bz)
    
def getFieldRz(R_coord, z_coord) :
    return getField(R_coord/R, z_coord/R)
    
def getFieldApprox( R_coord, z_coord ) :
    theta_coil=angle((R_coil-R)+1j*(z_coil-z_loop))
    R_dist=hypot(R_coil-R,z_coil-z)
    scale_fac=mu0*I/(2*pi*R_dist)
    return (-scale_fac*sin(theta_coil),scale_fac*cos(theta_coil))

R_coil=0.9
z_coil=0.2
z_loop=0.0

theta_coil=angle((R_coil-R)+1j*(z_coil-z_loop))

xbar=R_coil/R
zbar=z_coil/R

Rdist=sqrt(pow(R_coil-R,2)+pow(z_coil-z_loop,2)) #Euclidean norm between coil and loop current element in R,z plane

print("R_loop="+str(R)+" m, R_coil="+str(R_coil)+" m, z_coil="+str(z_coil)+" m")
print("xbar="+str(xbar)+", zbar="+str(zbar))

B_int_R,B_int_z=getField(xbar,zbar)
B_int=hypot(B_int_R,B_int_z)

BstraightConductor=mu0*I/(2*pi*Rdist) #Field around straight conductor
B_estim_R=-BstraightConductor*sin(theta_coil)
B_estim_z=BstraightConductor*cos(theta_coil)

print("-----------")
print("|B_integrate|="+str(B_int)+" T")
print("|B_straight|="+str(BstraightConductor)+" T")

print("B_integrate_R="+str(B_int_R)+" T")
print("B_straight_R="+str(B_estim_R)+" T")

print("B_integrate_z="+str(B_int_z)+" T")
print("B_straight_z="+str(B_estim_z)+" T")

#Get grid of points around coil
'''
Rgrid=linspace(R-0.2,R+0.2,100)
zgrid=linspace(-0.2,0.2,100)

RR,zz=meshgrid(Rgrid,zgrid)

B_grid=zeros(len(Rgrid),len(zgrid))
B_grid_approx=zeros(len(Rgrid),len(zgrid))

for ii in range(0,len(Rgrid)) :
    for jj in range(0,len(zgrid)) :
        B_grid[ii][jj]=getFieldRz(RR[ii][jj],zz[ii][jj])
        B_grid_approx[ii][jj]=getFieldApprox(RR[ii][jj],zz[ii][jj])
'''
#Calc field lines
'''
dR/BR=dz/Bz => z=int(dR Bz/BR)
R=cos(theta)*r
z=sin(theta)*r
BR = -sin(theta)*Btheta + cos(theta)*Br
Bz = cos(theta)*Btheta - sin(theta)*Br

[BR; Bz] = [cos(theta), -sin(theta); sin(theta), cos(theta)] [Br;Btheta]


[Br,Btheta] = [cos(theta), sin(theta); -sin(theta), cos(theta)][BR; Bz]

Br = cos(theta)*BR + sin(theta)*Bz
Btheta = -sin(theta)*BR +cos(theta)*Bz

dr/Br = r dtheta/Btheta => dr/r =  dtheta Br/Btheta => ln(r) = int(dtheta Br/Btheta) => r = exp(int(dtheta Br/Btheta))

dr/dtheta = r Br/Btheta
=>
r = int(dtheta r Br/Btheta)
'''

def changeB(BR, Bz, Rcoord, zcoord) :
    #print("changeB")
    theta=angle(Rcoord-R+1j*zcoord)
    Br=cos(theta)*BR + sin(theta)*Bz
    Btheta=-sin(theta)*BR+cos(theta)*Bz
    return (Br,Btheta)
    
def getBCyl(r,theta) :
    #print("getBCyl")
    this_R=r*cos(theta)+R
    this_z=r*sin(theta)
    BR,Bz=getFieldRz(this_R,this_z)
    Br,Btheta=changeB(BR,Bz,this_R,this_z)
    return Br,Btheta
    
def fieldLineDiffEq(theta, r) :
    #print("fieldLineDiffEq")
    Br,Btheta=getBCyl(r,theta)
    val=r*Br/Btheta
    return val #Return derivative of r with respect to theta on field line

def getFieldLine(R0, z0) :
    r0=abs(R0-R+1j*z0)
    theta0=angle(R0-R+1j*z0)
    theta_line=linspace(theta0,theta0+2*pi,50)
    r_line=zeros(len(theta_line))
    dtheta=theta_line[1]-theta_line[0]
    ode_obj=ode(fieldLineDiffEq).set_integrator('zvode', method='bdf', with_jacobian=False)
    ode_obj.set_initial_value(r0,theta0)
    for ii in range(0,len(theta_line)) :
        print("ii="+str(ii)+", theta="+str(theta_line[ii]))
        r_line[ii]=real(ode_obj.integrate(ode_obj.t+dtheta)[0])
        if(not ode_obj.successful() ) :
            print("Integration not successful at ii="+str(ii)+", theta="+str(theta_line[ii]*180.0/pi)+" deg")
            break
    
    return r_line, theta_line

R0=0.9
z0=0.0

r_line,theta_line=getFieldLine(R0,z0)

R_line=zeros(len(r_line))
z_line=zoros(len(r_line))

for ii in range(0,len(r_line)) :
    R_line[ii]=r_line[ii]*cos(theta_line[ii])
    z_line[ii]=r_line[ii]*sin(theta_line[ii])

my_figure=figure()
plot(R_line,z_line)
my_figure.show()

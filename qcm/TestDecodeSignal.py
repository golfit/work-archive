from decodeSignal import *
from numpy import *

#fpath="/media/USB DISK/qcm/MasterControllerBoardTests/C1SerialLogicTestN225to295kHzIn0pt5sGoesWithNclkTest.dat"
fpath="~data/ScopeData/C1SerialLogicTestN225to295kHzIn0pt5sGoesWithNclkTest.dat"
#Load data
dat=numpy.loadtxt(fpath)

print("Data loaded")

t=dat[:,0]
y=dat[:,1]

fclk=4.0E6/16.0

nbits=7

tpts,nums=decodeSignal(y,t,fclk,nbits)

print("decode finished")

print(tpts)
print(nums)

for i in range(0,len(tpts)):
	print( 't={0:f}, number={0:f}'.format(tpts[i], nums[i]) )

#This script is meant to load simulation data into a Matlab-readable data file
from geqdsk import Geqdsk
import scipy.io

#data_path='geqdsk'
data_path='gUse.geqdsk'

g=Geqdsk()

g.openFile(data_path)

all_data=g.data

for i in range(len(all_data)):
    #filename='1170514001geqdsk_t'+str(i)
    filename='diag_t'+str(i)
    print(filename)
    scipy.io.savemat(filename,all_data[i])

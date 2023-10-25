import numpy as np
import datetime
import matplotlib.pyplot as plt
import os
import glob
import sys
from fit_yb import *

from get_data import get_data, doppler2temp


kB = 1.38e-23
c = 299792458
amu = 1.6605e-27
hbar = 1.05457e-34




basefilename = '/home/molecules/software/data/20190620/20190620_'

options = {
        't1' : 10,
        't2' : 12,
        'nu1' : 300,
        'nu2' : 320
        }



result = []

# 0
result.append(get_data(time_stamp = '132513', options = options, basefilename = basefilename))
# 20
result.append(get_data(time_stamp = '143455', options = options, basefilename = basefilename))
# 40
result.append(get_data(time_stamp = '122803', options = options, basefilename = basefilename))
# 60
result.append(get_data(time_stamp = '140131', options = options, basefilename = basefilename))


x1 = 25
x2 = 31

mycolor = ['r', 'k', 'b', 'orange']

density = []
temps = []

plt.figure()
plt.subplot(3,1,1)
for k in range(len(result)):
    plt.plot(result[k]['nus'], result[k]['spectrum'], marker = 'o', markersize = 5, linestyle = '', color = mycolor[k])
    plt.plot(result[k]['x_fit'], result[k]['y_fit'], linestyle = '-', color = mycolor[k])
    plt.axvline(result[k]['nus'][x1])
    plt.axvline(result[k]['nus'][x2])
    

    density.append(np.mean(result[k]['spectrum'][x1:x2]))
    
    temps.append(doppler2temp(result[k]['fit_result'].params['w'] * 1e6, f0 = 2*375e12, mass = 171 * amu))

flow = np.array([0, 20, 40, 60])
density = np.array(density)
temps = np.array(temps)


plt.subplot(3,1,2)
for k in range(len(result)):
    plt.plot(flow/10.0, -density)
plt.xlabel('Flow (sccm)')
plt.ylabel('Signal (a.u.)')

plt.subplot(3,1,3)
for k in range(len(result)):
    plt.plot(flow/10.0, temps)
    
plt.xlabel('Flow (sccm)')
plt.ylabel('Temperature (K)')




plt.show()



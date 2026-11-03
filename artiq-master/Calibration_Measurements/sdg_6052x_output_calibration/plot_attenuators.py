import numpy as np
import pickle
import matplotlib.pyplot as plt

from fit_functions import fit_exp 

from scipy.interpolate import CubicSpline


def get_data(tag):

    freq_scan_arr = np.genfromtxt('out_scan_freq_{0}.csv'.format(tag), delimiter = ',')
    ampl_scan_arr = np.genfromtxt('out_scan_ampl_{0}.csv'.format(tag), delimiter = ',')
     
    
    with open("out_y_{0}.pkl".format(tag), "rb") as f:
        loaded_array = pickle.load(f)
    
    y3d = np.array(loaded_array)
    
    
    results = []
    
    for n in range(len(ampl_scan_arr)):
    
        hlp = []
        
        for t in range(len(freq_scan_arr)):
    
            freq = freq_scan_arr[t]
            ampl = ampl_scan_arr[n]
    
            val = np.max(y3d[n, t, :])
    
            #val_ampl = np.sqrt(10**(val/10))
    
            hlp.append(val)
    
        results.append(hlp)
    
    results = np.array(results)

    return (freq_scan_arr, ampl_scan_arr, results)


(f_arr, a_arr, res_awg_att) = get_data('only_awg_att_power_freq')
(f_arr, a_arr, res_all) = get_data('only_att_power_freq')





plt.figure()


for k in range(len(a_arr)):

    plt.subplot(3,1,1)
    plt.plot(f_arr, res_all[k, :])
    plt.subplot(3,1,2)
    plt.plot(f_arr, res_awg_att[k, :])
    plt.subplot(3,1,3)
    plt.plot(f_arr, res_all[k, :] - res_awg_att[k, :])


plt.xlabel('Frequency (MHz)')
plt.ylabel('(dB)')


plt.show()

asd



plt.figure()

for k in range(1, len(freq_scan_arr), 1):

    y = results[:, k]
    plt.plot(ampl_scan_arr, y, 'o')
    

plt.figure()

for k in [0, len(freq_scan_arr) - 1]:

    y = results[:, k]
    plt.plot(ampl_scan_arr, y, 'o', label = freq_scan_arr[k])
    
plt.legend()






plt.show()





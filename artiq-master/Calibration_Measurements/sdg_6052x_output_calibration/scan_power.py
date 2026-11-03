import os
import socket
import sys
import numpy as np
import time
import pickle

sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server")

from rigol import Rigol_RSA3030
from SDG_6052X import SDG_6052X


tag = 'amp_power_freq'

# Init instruments

spec = Rigol_RSA3030()

awg = SDG_6052X()


# configure awg

channel = 2
amplitude = 640e-3

awg.set_load(channel = channel, load = '50')
awg.set_sine_wave(channel = channel, frequency = 10e3, amplitude = amplitude)

awg.on(channel = channel)

# loop over calibration frequencies

scan_arr = np.linspace(0, 640e-3, 10)

scan_arr = np.insert(scan_arr, 1, 0.023)

freq_scan_arr = np.linspace(10.0, 500.0, 200)



delta = 3.0

# attenuation = 8.0
att = 8.0

# Start scan

results = []

for n in range(len(scan_arr)):

    hlp = []

    for t in range(len(freq_scan_arr)):

        print('Scan point {0:.3f} - {1:.1f}'.format(scan_arr[n], freq_scan_arr[t]))
    
        amplitude = scan_arr[n]
        
        freq = freq_scan_arr[t]

    
        # set the AWG output to the freq    
    
        #amplitude = 2.0 * np.sqrt(2.0) * np.sqrt(50 * 1e-3 * 10**( (pwr + att)/10.0 ) )
    
        awg.set_sine_wave(channel = channel, frequency = freq * 1e6, amplitude = amplitude)
    
        # set spectrum analyzer to zoom in on that frequency
        
        spec.set_freq([ (freq - delta) * 1e6 , (freq + delta) * 1e6])
    
        time.sleep(2)
    
    
        # download trace

        d = spec.get_trace()
    
        x = d[:, 0]
        y = d[:, 1]
    
        hlp.append(y)


    results.append(hlp)


results = np.array(results)


awg.off(channel = channel)



np.savetxt('out_scan_ampl_{0}.csv'.format(tag), scan_arr, delimiter = ',')
np.savetxt('out_scan_freq_{0}.csv'.format(tag), freq_scan_arr, delimiter = ',')

np.savetxt('out_x_{0}.csv'.format(tag), x, delimiter = ',')

# save 3d array
with open("out_y_{0}.pkl".format(tag), "wb") as f:
    pickle.dump(results, f, protocol = pickle.HIGHEST_PROTOCOL)

#np.savetxt('out_y_{0}.csv'.format(tag), results, delimiter = ',')





import os
import socket
import sys
import numpy as np
import time

sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server")

from rigol import Rigol_RSA3030
from SDG_6052X import SDG_6052X


tag = 'amp_components'

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

scan_arr = np.linspace(1.0, 500.0, 100)

delta = 3.0



# Start scan

results = []

for n in range(len(scan_arr)):

    print('Scan point {0}'.format(scan_arr[n]))

    freq = scan_arr[n]

    # set the AWG output to the freq    

    awg.set_sine_wave(channel = channel, frequency = freq* 1e6, amplitude = amplitude)

    # set spectrum analyzer to zoom in on that frequency
    
    spec.set_freq([ (freq - delta) * 1e6 , (freq + delta) * 1e6])

    time.sleep(2)



    d = spec.get_trace()

    x = d[:, 0]
    y = d[:, 1]

    results.append(y)


results = np.array(results)


awg.off(channel = channel)



np.savetxt('out_scan_{0}.csv'.format(tag), scan_arr, delimiter = ',')
np.savetxt('out_x_{0}.csv'.format(tag), x, delimiter = ',')
np.savetxt('out_y_{0}.csv'.format(tag), results, delimiter = ',')





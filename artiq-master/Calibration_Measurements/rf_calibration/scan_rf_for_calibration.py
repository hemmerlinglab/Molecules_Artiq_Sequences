import os
import socket
import sys
import numpy as np
import time

sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server")

from rigol import Rigol_RSA3030


# loop over calibration frequencies

scan_arr = np.linspace(-50.0, 11.0, 20)

freq = 25.0 # in MHz

delta = 20.0

attenuation = 0.0

tag = "{0:.0f}_30att_amp_20att".format(freq)



# Start scan

spec = Rigol_RSA3030()

spec.set_freq([ (freq - delta) * 1e6 , (freq + delta) * 1e6])

time.sleep(1)

results = []

for n in range(len(scan_arr)):

    print('Scan point {0}'.format(scan_arr[n]))

    x = scan_arr[n]

    os.system('cd ..; artiq_run -q Test_Functions/dds_test.py frequency={0} attenuation={1} amplitude_dBm={2}'.format(freq, attenuation, x))

    time.sleep(1)

    d = spec.get_trace()

    x = d[:, 0]
    y = d[:, 1]

    results.append(y)


results = np.array(results)


np.savetxt('out_scan_{0}.csv'.format(tag), scan_arr, delimiter = ',')
np.savetxt('out_x_{0}.csv'.format(tag), x, delimiter = ',')
np.savetxt('out_y_{0}.csv'.format(tag), results, delimiter = ',')




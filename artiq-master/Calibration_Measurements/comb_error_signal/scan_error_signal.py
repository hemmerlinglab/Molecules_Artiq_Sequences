import os
import socket
import sys
import numpy as np
import time

sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server")

from rigol_dho924 import Rigol_MHO98
from rigol import Rigol_DSG821

###########################################################################################
# Main
###########################################################################################

print('Connect DSG ...')
dsg = Rigol_DSG821(IP = '192.168.42.40')

print('Connect scope ...')
scope = Rigol_MHO98(IP = '192.168.42.86')

scope.init_scope_for_exp(channels = [2])

dsg.set_level(-15.0)
dsg.on()

# loop over calibration frequencies

scan_arr = np.linspace(1.0, 100.0, 50)

tag = 'both_maxpower'

# Start scan

results = []

for n in range(len(scan_arr)):

    print('Scan point {0}'.format(scan_arr[n]))

    x = scan_arr[n]

    dsg.set_freq(x)

    #time.sleep(1)

    (t, traces) = scope.read_channels(channels = [2], trigger = False)

    x = t
    y = traces[2]

    results.append(y)


dsg.off()


results = np.array(results)



np.savetxt('out_x_{0}.csv'.format(tag), scan_arr, delimiter = ',')
np.savetxt('out_y_{0}.csv'.format(tag), results, delimiter = ',')




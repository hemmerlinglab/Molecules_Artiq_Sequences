import os
import socket
import sys
import numpy as np
import time

sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server")

from rigol               import Rigol_RSA3030

import matplotlib.pyplot as plt

from calibrate_wavemeter import run_calibration

import pickle



offsets = np.linspace(-50, 50, 11)

results = []

for o in offsets:
    
    r = run_calibration(offset = o)

    results.append(r)


f = open('wavemeter_offset_calibration.pckl', 'wb')

pickle.dump([offsets, results], f)

f.close()



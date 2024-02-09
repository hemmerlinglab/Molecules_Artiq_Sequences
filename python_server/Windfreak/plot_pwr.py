import numpy as np

import matplotlib.pyplot as plt

date = '20240209'

time = '102023'

scan_filename = '/home/molecules/software/data/{0}/{0}_{1}'.format(date, time)


freq = np.genfromtxt(scan_filename + '_set_points', delimiter = ',')
spec = np.genfromtxt(scan_filename + '_beat_node_fft', delimiter = ',')

pwr = []
meas_freq = []

for k in range(len(freq)):

    xf = spec[2*k + 0, :]
    yf = spec[2*k + 1, :]


    ind = np.where(yf == np.max(yf))[0][0]

    pwr.append(yf[ind])
    meas_freq.append(xf[ind])


pwr = np.array(pwr)
meas_freq = np.array(meas_freq)


plt.figure()
plt.plot(freq, pwr)
plt.xlabel('Set Power (dBm)')
plt.ylabel('Measured Power (dBm)')

plt.show()



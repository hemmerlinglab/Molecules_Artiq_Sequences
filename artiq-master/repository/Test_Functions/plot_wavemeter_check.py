import numpy as np

import matplotlib.pyplot as plt


d = np.genfromtxt('wavemeter_check.csv', delimiter = ',')

base_freq = 384.228067 * 1e6

vc_comb1 = 282.869280 * 1e6
vc_comb2 = 282.869320 * 1e6

vc_offset = vc_comb1

x = d[:, 0] * 1e6
vl = d[:, 1] * 1e6
vc_wavemeter = d[:, 2] * 1e6

xl = np.linspace(min(x), max(x), 100) - base_freq

delta = x - base_freq


plt.figure()

plt.subplot(2,1,1)

plt.plot(delta, vl - base_freq, 'o-')

plt.plot(xl, xl, 'r--')

plt.axhline(0, ls = '--')

plt.xlabel('Calibration offset (MHz)')
plt.ylabel('Measured frequency Davos - base_freq (MHz)')

plt.subplot(2,1,2)
plt.plot(delta, vc_wavemeter - vc_offset, 'o')

plt.plot(delta, delta * 282/384 - 25.0, 'g--')

plt.axhline( vc_comb1 - vc_offset, ls = '--')
plt.axhline( vc_comb2 - vc_offset, ls = '--')

plt.plot(xl, xl, 'r--')

plt.xlabel('Calibration offset (MHz)')
plt.ylabel('Measured frequency Moglabs - offset_freq (MHz)')

plt.tight_layout()

plt.show()



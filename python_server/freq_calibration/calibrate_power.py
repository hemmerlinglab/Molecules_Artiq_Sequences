import numpy as np

import matplotlib.pyplot as plt


x = np.linspace(-20, 14, int((20+14)/2)+1)
y = [-22.96, -20.7, -18.9, -16.8, -14.8, -12.8, -10.8, -8.9, -6.9, -4.91, -2.92, -0.94, 0.94, 2.67, 4.1, 5.21, 5.87, 5.91]

base_file = 'final_power'

#base_file = 'windfreak_only/wf'

# actual values
m    = np.genfromtxt('{0}_markers.csv'.format(base_file), delimiter = ',')

m_freq = m[:, 0]
m_ampl = m[:, 1]

# set values
pwr_range    = np.genfromtxt('{0}_pwr_range.csv'.format(base_file), delimiter = ',')

plt.figure()

plt.plot(pwr_range, m_ampl, '.-')

plt.xlabel('SynthHD Set power (dBm)')
plt.ylabel('Amplitude (dBm) (+ 10 dBm power of the Agilent at 1.577 GHz')

plt.tight_layout()

plt.figure()

plt.plot(x, y, '.-')

plt.xlabel('Agilent Set power (dBm)')
plt.ylabel('Amplitude (dBm) (+ 6 dBm power of SynthHD at 13 GHz')

plt.tight_layout()



plt.show()

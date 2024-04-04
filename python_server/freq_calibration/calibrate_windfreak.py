import numpy as np

import matplotlib.pyplot as plt


base_file = 'mixer_zoom'

#base_file = 'windfreak_only/wf'

# spectra
x    = np.genfromtxt('{0}_spectra_freq_scale.csv'.format(base_file), delimiter = ',')
spec = np.genfromtxt('{0}_spectra.csv'.format(base_file), delimiter = ',')

# actual values
m    = np.genfromtxt('{0}_markers.csv'.format(base_file), delimiter = ',')

m_freq = m[:, 0]
m_ampl = m[:, 1]

# set values
freq_range    = np.genfromtxt('{0}_freq_range.csv'.format(base_file), delimiter = ',')


plt.figure()

plt.pcolor(spec)



plt.figure()

plt.plot(x[-1] - freq_range[-1], spec[-1])



plt.figure()

plt.subplot(2,1,1)
plt.plot(freq_range/1e6, m_freq - freq_range)

plt.xlabel('Set frequency (MHz)')
plt.ylabel('Set - Act frequency (Hz)')

plt.tight_layout()

plt.subplot(2,1,2)

plt.plot(freq_range/1e6, m_ampl)

plt.xlabel('Set frequency (MHz)')
plt.ylabel('Amplitude (dBm)')

plt.tight_layout()


plt.show()

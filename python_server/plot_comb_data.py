import numpy as np
import matplotlib.pyplot as plt

mytime = '155640'
mytime = '160537'
mytime = '160821'

d = np.genfromtxt('/home/molecules/software/data/20231025/20231025_' + mytime + '_beat_node_fft', delimiter = ',')

wm = np.genfromtxt('/home/molecules/software/data/20231025/20231025_' + mytime + '_act_freqs', delimiter = ',')

wm = 0.5 * wm * 1e12

x = d[0::2, :]
y = d[1::2, :]

frep_arr = np.genfromtxt('/home/molecules/software/data/20231025/20231025_' + mytime + '_frequency_comb_frep', delimiter = ',')

eom = np.genfromtxt('/home/molecules/software/data/20231025/20231025_' + mytime + '_EOM_frequency', delimiter = ',')

# subtract background
y = y #- np.mean(y, axis = 0)



# overall offset

offset = wm[-1]

# extract beat node

beat_freq = []
for k in range(len(y)):

    ind = np.where(y[k] == np.max(y[k]))[0][0]

    beat_freq.append(x[k][ind])

beat_freq = np.array(beat_freq)

plt.figure()
plt.subplot(4,1,1)
plt.pcolor(x[0]/1e6, range(len(x)), y)

plt.xlabel('Frequency (MHz)')

plt.tight_layout()


plt.subplot(4,1,2)


frep = 200.0e6

n_tooth = np.round(wm/frep)
#n_tooth = np.ceil(wm/frep)
n_tooth = np.floor(wm/frep)

meas_comb_freq = n_tooth * frep + beat_freq

plt.plot((wm - offset)/1e6, label = 'Wavemeter reading')

plt.plot((meas_comb_freq - offset)/1e6, label = 'Comb reading')

plt.legend()

plt.ylabel('Frequency (MHz) + {0:.2f}'.format(offset/1e12))

plt.tight_layout()

plt.subplot(4,1,3)

plt.plot(n_tooth - n_tooth[0])

plt.tight_layout()

plt.subplot(4,1,4)
plt.plot(frep_arr - frep)
plt.tight_layout()

plt.ylabel('Comb freq')

plt.show()


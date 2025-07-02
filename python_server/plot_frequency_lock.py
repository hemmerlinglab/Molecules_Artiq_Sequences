import numpy as np
import matplotlib.pyplot as plt






spec = np.genfromtxt('freq_spec.txt', delimiter = ',')

err = np.genfromtxt('freq_err.txt', delimiter = ',')

wm = np.genfromtxt('freq_wm.txt', delimiter = ',')

nu = np.mean(wm)

plt.figure()

plt.subplot(3,1,1)

freq_scale = spec[0, :]
spec2D = spec[1::2, :]

n_exp = range(spec2D.shape[0])

plt.pcolor(freq_scale / 1e6, n_exp, spec2D)

plt.xlabel('Beat Node (MHz)')
plt.ylabel('Time')

plt.subplot(3,1,2)

#err2D = err

#plt.pcolor(err2D)


err_avg = np.mean(err, axis = 1)
err_std = np.std(err, axis = 1)

plt.plot(err_avg, n_exp, '.')
plt.plot(err_avg + err_std, n_exp, 'r.')
plt.plot(err_avg - err_std, n_exp, 'r.')


plt.subplot(3,1,3)

plt.plot((wm - nu) * 1e6, n_exp, '.')

plt.tight_layout()

plt.show()





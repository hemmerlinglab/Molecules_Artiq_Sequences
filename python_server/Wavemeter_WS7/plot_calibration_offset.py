import pickle

import numpy as np

import matplotlib.pyplot as plt

f = open('wavemeter_offset_calibration.pckl', 'rb')

arr = pickle.load(f)

f.close()


x = arr[0]

y = np.array(arr[1])

ml = y[:, 1]
tisaph = y[:, 0]


plt.subplot(2,1,1)

plt.plot(x, ml - np.mean(ml))

plt.plot(x, tisaph - np.mean(tisaph))

plt.subplot(2,1,2)

plt.plot(x, ml/tisaph)

r = np.mean(ml/tisaph)

plt.ylim(r - 1e-7, r + 1e-7)

print('{0:2f}'.format(r))



plt.show()




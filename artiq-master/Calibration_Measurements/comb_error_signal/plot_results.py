import numpy as np

import matplotlib.pyplot as plt


def get_data(tag = ''):

    x = np.genfromtxt('out_x_{0}.csv'.format(tag), delimiter = ',')
    y = np.genfromtxt('out_y_{0}.csv'.format(tag), delimiter = ',')
    
    y_m = np.mean(y, axis = 1)

    return (x, y_m)

plt.figure()

(x2, y2) = get_data(tag = '2cyc')
(x4, y4) = get_data(tag = '4cyc')
(x7, y7) = get_data(tag = '7cyc')

(x, y) = get_data(tag = 'both')
(xm, ym) = get_data(tag = 'both_maxpower')


new_sig = 30*y2+0*y7

new_sig = np.array([ np.min([1.0, np.max([-1.0, new_sig[k]])]) for k in range(len(new_sig)) ])

plt.plot(x2, y2)
plt.plot(x4, y4)
plt.plot(x7, y7)
plt.plot(x, y)
plt.plot(xm, ym, '--')
#plt.plot(x, new_sig)

plt.xlabel('Beat node frequency (MHz)')
plt.ylabel('Error signal (V)')

plt.show()



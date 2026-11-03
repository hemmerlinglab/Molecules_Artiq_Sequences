import numpy as np
import matplotlib.pyplot as plt

from fit_functions import fit_exp 


def get_data(tag):

    scan_arr = np.genfromtxt('out_scan_{0}.csv'.format(tag), delimiter = ',')
    x = np.genfromtxt('out_x_{0}.csv'.format(tag), delimiter = ',')
    y2d = np.genfromtxt('out_y_{0}.csv'.format(tag), delimiter = ',')
 
    y2d = np.transpose(y2d)
    
    # cut the dc part
    y2d = y2d[10:, :]

    delta_freq = x[10:]/1e6
    
    delta = 5.0
    
    delta_freq = np.linspace(-delta, delta, len(delta_freq))
    
    # get amplitude as a function of frequency
    
    max_val = np.max(y2d, axis = 0)

    ax = 0

    return (ax, scan_arr, max_val)



(ax, scan_arr, max_val) = get_data('amp_power')

plt.subplot(2,1,2)

x = scan_arr

y = np.sqrt(10**(max_val/10))

plt.plot(scan_arr, y/y[-1], 'o-')


(result, xf, yf, residuals) = fit_exp(x, y/y[-1])

print(result)

plt.plot(xf, yf, 'r--')

plt.subplot(2,1,1)
plt.plot(scan_arr, max_val, 'o-')

plt.plot(xf, np.log10(yf**2)*10.0 - 10.7)


# y_fit = x/(1 + x/0.85 * 2*p)**(1/(2*p))
# np.log10( (x/(1 + x/0.85 * 2*p)**(1/(2*p)))**2 * 10.0 )


plt.show()




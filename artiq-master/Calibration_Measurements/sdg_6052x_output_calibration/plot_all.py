import numpy as np
import pickle
import matplotlib.pyplot as plt

from fit_functions import fit_exp 

from scipy.interpolate import CubicSpline


#tag = 'amp_power_freq'

#tag = 'ampl_minus2dB_power_freq'

tag = 'ampl_minus3dB_power_freq'

freq_scan_arr = np.genfromtxt('out_scan_freq_{0}.csv'.format(tag), delimiter = ',')
ampl_scan_arr = np.genfromtxt('out_scan_ampl_{0}.csv'.format(tag), delimiter = ',')


#x = np.genfromtxt('out_x_{0}.csv'.format(tag), delimiter = ',')

#y2d = np.genfromtxt('out_y_{0}.csv'.format(tag), delimiter = ',')
 

with open("out_y_{0}.pkl".format(tag), "rb") as f:
    loaded_array = pickle.load(f)

y3d = np.array(loaded_array)




results = []

for n in range(len(ampl_scan_arr)):

    hlp = []
    
    for t in range(len(freq_scan_arr)):

        freq = freq_scan_arr[t]
        ampl = ampl_scan_arr[n]

        val = np.max(y3d[n, t, :])

        val_ampl = np.sqrt(10**(val/10))

        hlp.append(val_ampl)

    results.append(hlp)

results = np.array(results)

plt.figure()

plt.pcolor(freq_scan_arr, ampl_scan_arr, results)

plt.xlabel('Frequency (MHz)')
plt.ylabel('AWG amplitude (V)')


# fit ampl

f_xf = []
f_yf = []

fit_pars = []

for n in range(len(freq_scan_arr)):

    x = ampl_scan_arr 
    y = results[:, n]

    # transform to amplitude

    #y = np.sqrt(10**(results[:, n]/10))

    (result, xf, yf, residuals) = fit_exp(x, y)

    fit_pars.append(result.params)

    f_xf.append(xf)
    f_yf.append(yf)

f_xf = np.array(f_xf)
f_yf = np.array(f_yf)


plt.figure()

for k in range(1, f_xf.shape[0], 1):

    y = results[:, k]
    plt.plot(ampl_scan_arr, y, 'o')
    
    plt.plot(f_xf[k, :], f_yf[k, :], '--')

#figure 3 
plt.figure()

for k in [0, f_xf.shape[0]-1]:

    y = results[:, k]
    plt.plot(ampl_scan_arr, y, 'o', label = "{0:.1f} MHz".format(freq_scan_arr[k]))
    
    plt.plot(f_xf[k, :], f_yf[k, :], '--')

plt.legend()

plt.xlabel('Amplitude in (V)')
plt.ylabel('Amplitude out (V)')




#const_ampl = 0.2383 #results[-1, -1]
# const_ampl = 0.266 #results[-1, -1]

# get the minimum of the frequency scan of the last amplitude
const_ampl = np.min(results[-1, :])



corr_ampl = []


for k in range(len(freq_scan_arr)):

    (xf, yf) = (f_xf[k], f_yf[k])

    ind = np.where( abs(const_ampl - yf) < 0.004 )[0][0]
    
    # input amplitude at which the output amplitude = const_ampl
    corr_ampl.append([freq_scan_arr[k], xf[ind]])



#figure 4

plt.figure()

for k in range(len(ampl_scan_arr)):

    y = results[k, :]

    plt.plot(freq_scan_arr, y, '-')
            
plt.xlabel('Frequency (MHz)')
plt.ylabel('Value')

corr_ampl = np.array(corr_ampl)


max_amplitude = 640e-3

#figure 5
plt.figure()
plt.plot(freq_scan_arr, corr_ampl[:, 1]/max_amplitude, 'o-')

plt.xlabel('Frequency (MHz)')
plt.ylabel('Value')


#################################
# interpolate with a spline
#################################

x_spline = freq_scan_arr
y_spline = corr_ampl[:, 1]/max_amplitude

cs = CubicSpline(x_spline, y_spline)

x_new = np.linspace(10, 500, 1000)

plt.plot(x_new, cs(x_new), 'r--')

plt.xlabel('Frequency (MHz)')
plt.ylabel('Input amplitude corr (V)')


with open("amplifier_spline.pkl", "wb") as f:
    pickle.dump(cs, f)

#################################


Gs = [x['G'].value for x in fit_pars]
ps = [x['p'].value for x in fit_pars]
Vsats = [x['Vsat'].value for x in fit_pars]

#figure 6
plt.figure()
plt.plot(freq_scan_arr, Gs, label = 'G')
plt.plot(freq_scan_arr, ps, label = 'p')
plt.plot(freq_scan_arr, Vsats, label = 'Vsat')

plt.xlabel('Frequency (MHz)')
plt.ylabel('Value')

plt.legend()

plt.show()





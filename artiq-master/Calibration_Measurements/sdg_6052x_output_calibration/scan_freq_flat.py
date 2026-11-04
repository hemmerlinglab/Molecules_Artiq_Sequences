import os
import socket
import sys
import numpy as np
import time
import pickle
import matplotlib.pyplot as plt

sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server")

from rigol import Rigol_RSA3030
from SDG_6052X import SDG_6052X


tag = 'amp_new_2'


# load cali

########################################
# correction for the attenuators
########################################

c = np.genfromtxt('calib_data.csv', delimiter = ',')

c_freq = c[0, :]
c_ampl = c[1, :]

c_corr_dB = min(c_ampl) - c_ampl

# the factor of 2.0 is there since it is an amplitude, not a power correction
c_corr_ampl = 10**(c_corr_dB/10.0/2.0)


########################################
# correction for the amplifier
########################################

c_amp = np.genfromtxt('amp_calib_data.csv', delimiter = ',')

c_amp_freq = c_amp[0, :]
c_amp_ampl = c_amp[1, :]

c_amp_corr_dB = min(c_amp_ampl) - c_amp_ampl

# the factor of 2.0 is there since it is an amplitude, not a power correction
c_amp_corr_ampl = 10**(c_amp_corr_dB/10.0/2.0)


with open("amplifier_spline.pkl", "rb") as f:
    amp_spline = pickle.load(f)

f = np.linspace(10, 500, 100)

plt.plot(f, amp_spline(f))

#plt.subplot(2,2,1)
#plt.plot(c_freq, c_ampl)
#plt.plot(c_freq, c_corr_dB)
#
#plt.subplot(2,2,3)
#plt.plot(c_freq, c_corr_ampl)
#
#plt.subplot(2,2,2)
#plt.plot(c_amp_freq, c_amp_ampl)
#plt.plot(c_amp_freq, c_amp_corr_dB)
#
#plt.subplot(2,2,4)
#plt.plot(c_amp_freq, c_amp_corr_ampl)

#plt.show()

#asd

# Init instruments

spec = Rigol_RSA3030()

awg = SDG_6052X()


# configure awg

channel = 2
max_amplitude = 640e-3

awg.set_load(channel = channel, load = '50')
awg.set_sine_wave(channel = channel, frequency = 10e3, amplitude = max_amplitude)

awg.on(channel = channel)

# loop over calibration frequencies

scan_arr = np.linspace(10.0, 500.0, 200)

delta = 3.0


# Start scan

results = []

for n in range(len(scan_arr)):

    print('Scan point {0}'.format(scan_arr[n]))

    freq = scan_arr[n]

    ## set the AWG output to the freq    

    #ind_c = np.where( np.abs(freq - c_freq) < 3.0 )[0][0]
    #
    #ind_a = np.where( np.abs(freq - c_amp_freq) < 3.0 )[0][0]

    #corr_fac = c_amp_corr_ampl[ind_a] * c_corr_ampl[ind_c]

    ## freq corr amplitude
    #freq_corr_amplitude = corr_fac * max_amplitude

    ## gain corr amplitude
    #G = 2.8
    #Vsat = 1.03
    #p = 1.87

    #gain_corr = lambda x : G * x/(1 + np.abs(G * x/Vsat)**(2 * p))**(1/(2*p))

    #final_amplitude = freq_corr_amplitude * gain_corr(freq_corr_amplitude)

    final_amplitude = max_amplitude * amp_spline(freq)
    #final_amplitude = max_amplitude 

    print('Amplitude {0:.3f} = {1:.3f} * {2:.3f}'.format(final_amplitude * 1e3, max_amplitude * 1e3, amp_spline(freq)))

    awg.set_sine_wave(channel = channel, frequency = freq * 1e6, amplitude = final_amplitude)

    # set spectrum analyzer to zoom in on that frequency
    
    spec.set_freq([ (freq - delta) * 1e6 , (freq + delta) * 1e6])

    time.sleep(2)



    d = spec.get_trace()

    x = d[:, 0]
    y = d[:, 1]

    results.append(y)


results = np.array(results)


awg.off(channel = channel)



np.savetxt('out_scan_{0}.csv'.format(tag), scan_arr, delimiter = ',')
np.savetxt('out_x_{0}.csv'.format(tag), x, delimiter = ',')
np.savetxt('out_y_{0}.csv'.format(tag), results, delimiter = ',')





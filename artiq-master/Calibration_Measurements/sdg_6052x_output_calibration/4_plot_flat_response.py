import numpy as np
import matplotlib.pyplot as plt


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


##############################################
# Main
##############################################

# get uncorrected amplitudes from AWG
(ax, scan_arr, max_val) = get_data(0)

# awg: 8dB att, output of amp with 50 dB attenuation at spectrum analyzer
(ax3, scan_arr_amp, max_val_amp) = get_data('amp')

# awg: 6dB att, output of amp with 50 dB attenuation at spectrum analyzer
(ax3, scan_arr_amp_flat_6dB, max_val_amp_flat_6dB) = get_data('amp_new')

# awg: 5dB att, output of amp with 50 dB attenuation at spectrum analyzer
(ax3, scan_arr_amp_flat_5dB, max_val_amp_flat_5dB) = get_data('amp_new_2')

# awg: 5dB att, output of amp with 50 dB attenuation at spectrum analyzer
(ax3, scan_arr_amp_sw_flat_5dB, max_val_amp_sw_flat_5dB) = get_data('amp_and_switch')






###########################
# Plots
###########################

spec_att = 50.0 # 50 dB at input of spectrum analyzer

(fig, ax) = plt.subplots(2, 1)

ax[0].plot(scan_arr, max_val, label = 'awg -> 8dB')

ax[1].plot(scan_arr_amp, max_val_amp + spec_att, label = 'awg -> 8dB -> amp (uncorr)')

ax[1].plot(scan_arr_amp_flat_6dB, max_val_amp_flat_6dB + spec_att, label = 'awg -> 6dB -> amp (flattened)')

ax[1].plot(scan_arr_amp_flat_5dB, max_val_amp_flat_5dB + spec_att, label = 'awg -> 5dB -> amp (flattened)')

ax[1].plot(scan_arr_amp_sw_flat_5dB, max_val_amp_sw_flat_5dB + spec_att, label = 'awg -> rf switch -> 4dB -> amp (flattened)')

ax[1].axhline(39, ls = '--', color = 'k')

ax[0].legend()
ax[1].legend()

ax[1].set_ylim(35, 40)

ax[1].set_xlabel('Frequency (MHz)')
ax[0].set_ylabel('Power out (dBm)')
ax[1].set_ylabel('Power out (dBm)')

plt.show()





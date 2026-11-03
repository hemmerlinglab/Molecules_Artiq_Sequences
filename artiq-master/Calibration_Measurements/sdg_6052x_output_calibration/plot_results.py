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


    #(fig, ax) = plt.subplots(2,1)  
    
    #ax[0].pcolor(scan_arr, delta_freq, y2d)
    #
    #ax[0].set_ylabel('Relative freq (MHz)')
    #
    #ax[1].plot(scan_arr, max_val, label = tag)
    #ax[1].set_xlabel('AWG Frequency (MHz)')
    #
    #ax[1].set_ylabel('Power at amplifier input (dBm)')

    #ax[0].set_title('Tag {0}'.format(tag))

    #ax[1].legend()

    ax = 0

    return (ax, scan_arr, max_val)


# get uncorrected amplitudes

(ax, scan_arr, max_val) = get_data(0)

# calibration of attenuators and cables
calib_data = np.array([scan_arr, max_val])

np.savetxt('calib_data.csv', calib_data, delimiter = ',')


# get corrected amplitudes
(ax2, scan_arr_flat, max_val_flat) = get_data('flat')

# with 50 dB attenuation at spectrum analyzer
(ax3, scan_arr_amp, max_val_amp) = get_data('amp')

(ax3, scan_arr_amp_flat_new, max_val_amp_flat_new) = get_data('amp_new')

# correct ampl and with 50 dB attenuation at spectrum analyzer
(ax4, scan_arr_amp_flat, max_val_amp_flat) = get_data('amp_flat')

(ax5, scan_arr_cmp, max_val_cmp) = get_data('components')

(ax5, scan_arr_cmp_flat, max_val_cmp_flat) = get_data('components_flat')

(ax6, scan_arr_amp_cmp_flat, max_val_amp_cmp_flat) = get_data('amp_components_flat')


# calibration of amplifier frequency dependence

scan_arr_amp_flat = scan_arr_amp_flat[2:]
max_val_amp_flat = max_val_amp_flat[2:]

amp_calib_data = np.array([scan_arr_amp_flat, max_val_amp_flat])

np.savetxt('amp_calib_data.csv', amp_calib_data, delimiter = ',')


(fig, ax) = plt.subplots(1, 1)

ax.plot(scan_arr, max_val, label = 'awg')

#ax.plot(scan_arr_flat, max_val_flat, label = 'awg flat')

ax.plot(scan_arr_amp, max_val_amp, label = 'amp (50 dB att)')

#ax.plot(scan_arr_amp_flat, max_val_amp_flat, label = 'amp_flat')

#ax.plot(scan_arr_cmp, max_val_cmp, label = 'cmp')

#ax.plot(scan_arr_cmp_flat, max_val_cmp_flat, label = 'cmp_flat')

ax.plot(scan_arr_amp_cmp_flat, max_val_amp_cmp_flat, label = 'amp_cmp_flat (50 dB att)')

ax.plot(scan_arr_amp_flat_new, max_val_amp_flat_new, label = 'amp_cmp_flat new (50 dB att)')

ax.axhline(39 - 50, ls = '--', color = 'k')

ax.legend()

ax.set_ylim(-14, -7)

plt.show()




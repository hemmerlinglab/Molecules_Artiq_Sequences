import numpy as np

import matplotlib.pyplot as plt


def get_data(tag):

    x = np.genfromtxt('out_x_{0}.csv'.format(tag), delimiter = ',')
    y = np.genfromtxt('out_y_{0}.csv'.format(tag), delimiter = ',')

    scan_arr = np.genfromtxt('out_scan_{0}.csv'.format(tag), delimiter = ',')

    x = x/1e6

    return {tag : { 'x' : x, 'y' : y, 'scan_arr' : scan_arr}}


def extract_peak_height(y):

    # extract height of peaks in 2D array

    peak_height = []

    for n in range(len(y)):

        peak_height.append(np.max(y[n, :]))

    return np.array(peak_height)


def process_data(tags = []):

    results = {}

    for k in range(len(tags)):

        tag = tags[k]
        
        d = get_data(tag)
        
        (x, y, scan_arr) = d[tag].values()
        
        y_heights = extract_peak_height(y)

        results[tag] = {'x' : x, 'y' : y, 'y_heights' : y_heights}

    results['scan_arr'] = scan_arr

    return results


tags = ['25', '75', '375', '425', '25_att', '25_30att', '25_30att_amp_20att']

results = process_data(tags)


# amplitude scan

plt.figure()

for t in tags:

    offset = 0

    if t == '25_30att_amp_20att':

        # adding 20 dB to cancel out the added attenuators in front of the spec analyzer
        offset = +20.0

    plt.plot(results['scan_arr'], results[t]['y_heights'] + offset, 'o', label = '{0} MHz'.format(t))

a = np.linspace(-50, 11)

plt.plot(a, a)

plt.xlabel('DDS Amplitude (dBm)')
plt.ylabel('Measured Peak power (dBm)')

plt.legend()


# single frequency plot

plt.figure()


for n, t in enumerate(tags):

    plt.plot(results[t]['x'] - np.mean(results[t]['x']), results[t]['y'][-1] + 70 * n, '-', label = '{0} MHz'.format(t))

plt.legend()

plt.show()





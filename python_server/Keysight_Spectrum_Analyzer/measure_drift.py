import numpy as np

import matplotlib.pyplot as plt
from keysight import Keysight








x_arr = []
y_arr = []




low_freq = 10e6 
high_freq = 250e6 
high_freq = 210e6


no_of_scans = 300

span_freq = high_freq - low_freq
cnt_freq = (high_freq + low_freq)/2.0


results = []
for k in range(no_of_scans):
    try:
        spec = Keysight()

        spec.set_center_freq(cnt_freq)
        spec.set_span(span_freq)


        spec.set_sweep()
        d = spec.get_trace()
        spec.close()

        if len(d) == 1000:
            results.append(d)
    except:
        pass

results = np.array(results)

no_of_scans = results.shape[0]

#no = 3
#
#f = open('spec_data_x_' + str(no) + '.csv', 'w')
#np.savetxt(f, x_arr, delimiter=",")
#f.close()
#
#f = open('spec_data_y_' + str(no) + '.csv', 'w')
#np.savetxt(f, y_arr, delimiter=",")
#f.close()

xscale = np.linspace(low_freq, high_freq, 1001) / 1e6

xscale = xscale[:-1]




f = open('freq_drift_x.csv', 'w')

np.savetxt(f, xscale, delimiter = ',')

f.close()

f = open('freq_drift_y.csv', 'w')

np.savetxt(f, results, delimiter = ',')

f.close()






plt.figure()


plt.subplot(2,1,1)
plt.pcolor(xscale, np.arange(no_of_scans), results)
plt.subplot(2,1,2)
plt.plot(xscale, results[0, :])

plt.show()







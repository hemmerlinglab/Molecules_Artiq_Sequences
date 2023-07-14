import numpy as np

import matplotlib.pyplot as plt
from keysight import Keysight






x_arr = []
y_arr = []




low_freq = 1e6 
high_freq = 220e6

no_of_scans = 200

span_freq = high_freq - low_freq
cnt_freq = (high_freq + low_freq)/2.0

no_of_scans = 2

results = []

spec = Keysight()

spec.set_center_freq(cnt_freq)
spec.set_span(span_freq)

spec.set_sweep()

d = []

(m1, m2, m3) = spec.do_peak_search()

print('Getting trace ...')
d = spec.get_trace()


print('marker1')
print(m1)
print('marker1')
print(m2)
print(m3)

#print(d)

spec.close()


x = np.linspace(low_freq, high_freq, len(d))/1e6
y = d

plt.plot(x, y)

#plt.plot(y)

plt.ylim(-100, 0)
plt.show()


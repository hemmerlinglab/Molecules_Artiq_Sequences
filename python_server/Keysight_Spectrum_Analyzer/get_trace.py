import numpy as np

import matplotlib.pyplot as plt
from keysight import Keysight






x_arr = []
y_arr = []




low_freq = 10e6 
high_freq = 210e6

no_of_scans = 200

span_freq = high_freq - low_freq
cnt_freq = (high_freq + low_freq)/2.0

no_of_scans = 2

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

print(results.shape)

plt.plot(results[0])

plt.show()


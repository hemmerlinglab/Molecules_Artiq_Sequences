import numpy as np

import sys
import time

import matplotlib.pyplot as plt

sys.path.append("Windfreak")

from Windfreak.microwave_windfreak import Microwave

#from Keysight_Spectrum_Analyzer.keysight import Keysight
from Keysight_Spectrum_Analyzer.keysight_used_for_scan import Keysight

span_freq = 1.0e3 # Hz
bw_freq = 1.0e3 # Hz


xscale = [] #np.linspace(low_freq, high_freq, 1001) / 1e6


#freq_range = np.linspace(15.0e6, 15.0e9, 100)

#freq_range = np.array([10.0e6, 100.0e6, 113.0e6])


freq_range = np.linspace(13.0e9 - 10e6, 13.0e9 + 10e6, 30)


xscales = []


mw = Microwave()


mw.power(0)

mw.on()

result = []

markers = []

marker_measure = []



k = 0

while k < len(freq_range):

    try:
        
        spec = Keysight()

        spec.set_span(span_freq)

        nu = freq_range[k]

        print('Current frequency {0}'.format(nu))

        mw.freq(nu)

        
        #spec.set_center_freq(nu)

        # for mixer
        
        spec.set_center_freq(nu + 1.5e9)

        
        time.sleep(1)

        spec.set_sweep()

        time.sleep(1)

        m = spec.do_peak_search()
        
        m_meas = spec.marker_measure(1)        
        
        d = spec.get_trace()
        
        if len(d) == 1000:
                result.append(d)
        
                markers.append(m)

                marker_measure.append(m_meas)

                low_freq  = nu - span_freq/2.0
                high_freq = nu + span_freq/2.0

                tmp = np.linspace(low_freq, high_freq, 1001)
                xscale.append(tmp[:-1])

        spec.close()

        repeat = False
        
        k = k + 1

    except:

        print('Repeating point')

        repeat = True

mw.off()

spec = Keysight()
spec.send(':INIT:CONT ON')
spec.close()

#print(marker_measure)

result = np.array(result)

markers = np.array(markers)

marker_measure = np.array(marker_measure)


base_file = 'mixer_zoom'


f = open('freq_calibration/{0}_markers.csv'.format(base_file), 'w')

np.savetxt(f, marker_measure, delimiter = ',')

f.close()

f = open('freq_calibration/{0}_spectra.csv'.format(base_file), 'w')

np.savetxt(f, result, delimiter = ',')

f.close()

f = open('freq_calibration/{0}_spectra_freq_scale.csv'.format(base_file), 'w')

np.savetxt(f, xscale, delimiter = ',')

f.close()

f = open('freq_calibration/{0}_freq_range.csv'.format(base_file), 'w')

np.savetxt(f, freq_range, delimiter = ',')

f.close()








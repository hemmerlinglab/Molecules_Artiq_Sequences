import numpy as np

import sys
import time

import matplotlib.pyplot as plt

sys.path.append("Windfreak")

from Windfreak.microwave_windfreak import Microwave

from Keysight_Spectrum_Analyzer.keysight_used_for_scan import Keysight





pwr_range = np.linspace(-50, 10, 30)



mw = Microwave()


mw.freq(13.0e9)
mw.power(-50)

mw.on()


marker_measure = []



k = 0

while k < len(pwr_range):

    try:
        
        spec = Keysight()

        nu = pwr_range[k]

        print('Current power {0}'.format(nu))

        mw.power(nu)

        time.sleep(1)

        #spec.set_sweep()

        #time.sleep(1)

        #m = spec.do_peak_search()
        
        m_meas = spec.marker_measure(1)        
        
        marker_measure.append(m_meas)

        #d = spec.get_trace()
        #
        #if len(d) == 1000:
        #        result.append(d)
        #
        #        markers.append(m)

        #        marker_measure.append(m_meas)

        #        low_freq  = nu - span_freq/2.0
        #        high_freq = nu + span_freq/2.0

        #        tmp = np.linspace(low_freq, high_freq, 1001)
        #        xscale.append(tmp[:-1])

        spec.close()

        repeat = False
        
        k = k + 1

    except:

        print('Repeating point')

        repeat = True
        
        asd
mw.off()


marker_measure = np.array(marker_measure)



base_file = 'final_power'


f = open('freq_calibration/{0}_markers.csv'.format(base_file), 'w')

np.savetxt(f, marker_measure, delimiter = ',')

f.close()

f = open('freq_calibration/{0}_pwr_range.csv'.format(base_file), 'w')

np.savetxt(f, pwr_range, delimiter = ',')

f.close()








import numpy as np
import time

from base_instruments import base_visa_instrument


# Rigol Spectrum Analyzer

class Rigol_DHO924(base_visa_instrument):
 
    def __init__(self, IP = '192.168.42.41'):

        # call constructor of parent class
        super().__init__(IP)

        return

    def get_id(self):

        s = self.query('*IDN?')

        print(s)
        
        return

    def get_trace(self, ch):

        self.write(':WAV:SOURCE CHAN{0}'.format(ch))
        
        self.write(':WAV:FORMAT ASCII')

        d = self.query(':WAV:DATA?')

        data = [float(x) for x in d.split(',')]

        return np.array(data)

    def set_freq(self, freq_interval):
        # freq_interval = [40.0, 500.0]

        self.write('*OPC')

        self.write(':SENSE:FREQ:START {0:.6f}'.format(freq_interval[0]))
        self.write(':SENSE:FREQ:STOP {0:.6f}'.format(freq_interval[1]))

        self.wait_finished()

        return


##################################################################################################
# Main
##################################################################################################

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    s = Rigol_DHO924()

    s.get_id()

    d0 = s.get_trace(1)
    d1 = s.get_trace(2)

    time.sleep(1)
    plt.plot(d0/max(d0))
    plt.plot(d1/max(d1))
    plt.show()

    s.close()




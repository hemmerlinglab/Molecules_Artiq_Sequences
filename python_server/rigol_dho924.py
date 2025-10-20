import numpy as np
import time

from base_instruments import base_visa_instrument


# Rigol Scope DHO924

class Rigol_DHO924(base_visa_instrument):
 
    def __init__(self, IP = '192.168.42.41'):

        # call constructor of parent class
        super().__init__(IP)

        #print('Clearing event register')
        self.write('*CLS')

        #self.get_id()
        
        return

    def get_id(self):

        s = self.query('*IDN?')

        print(s)
        
        return

    def init_scope_for_exp(self, channels = [1]):

        self.write(':WAVEFORM:MODE NORMAL')
        self.write(':WAVEFORM:FORMAT ASCII')
        self.write(':WAVEFORM:POINTS 1000')
        
        self.write(':ACQ:MDEPTH 100k')

        # switch on/off channels
        for ch in [1, 2, 3, 4]:

            if ch in channels:
                self.write('CHANNEL{0}:DISPLAY ON'.format(ch))
            else:
                self.write('CHANNEL{0}:DISPLAY OFF'.format(ch))

        # get x scale

        self.x_inc    = float(self.query(':WAVEFORM:XINC?'))
        self.x_offset = float(self.query(':WAVEFORM:XORIGIN?'))
        

        return

    def read_channels(self, channels = [1]):

        traces = {}

        # take a single trigger
        self.write(':SINGLE')

        # wait for trigger to finish
        self.write('*WAI')
        
        for ch in channels:
            
            # activate channel
            self.write(':WAV:SOURCE CHAN{0}'.format(ch))

            waveform_str = self.query(':WAV:DATA?')
            
            traces[ch] = np.array([float(val) for val in waveform_str.strip().split(',')])

        # saves the common time array using the first channel
        t = (np.arange(len(traces[channels[0]])) * self.x_inc) + self.x_offset
        
        return (t, traces)

    def read_all_channels(self):

        (t, traces) = self.read_channels(channels = [1, 2, 3, 4])

        data = [t]
        data.append(traces[1])
        data.append(traces[2])
        data.append(traces[3])
        data.append(traces[4])

        return np.array(data)

    def plot_traces(self, t, traces):

        plt.figure()
        
        for k in range(traces.shape[0]):
            plt.plot(t, traces[k], label = k)

        plt.legend()

        return


##################################################################################################
# Main
##################################################################################################

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    s = Rigol_DHO924()

    #s.get_id()

    ch = [1, 2, 3, 4]

    s.init_scope_for_exp(channels = ch)

    d = s.read_all_channels()

    print(d.shape)

    s.plot_traces(d[0, :], d[1:, :])

    plt.show()

    s.close()



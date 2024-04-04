# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime
import os
import time
import csv

import sys
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")

from base_functions import *
from base_sequences import *
from helper_functions import *


# This sequence locks the laser to the wavemeter
# and scans the microwave

# every Experiment needs a build and a run function
class Test_Microwave(EnvExperiment):

    def build(self):
        base_build(self, which_instruments = ['microwave', 'spectrum_analyzer'])
        self.sequence_filename = os.path.abspath(__file__)

        pulsed_scan_build(self)

        # additional attributes
        my_setattr(self, 'microwave_power', NumberValue(default = -50,unit='dB',scale=1,ndecimals=1,step=1))
        
        return

    def prepare(self):
        # function is run before the experiment, i.e. before run() is called

        self.set_dataset('in_cell_spectrum',     ([0] * self.setpoint_count),broadcast=True)
        self.set_dataset('pmt_spectrum',         ([0] * self.setpoint_count),broadcast=True)

        self.scan_interval = np.linspace(self.setpoint_min, self.setpoint_max, self.setpoint_count)

        my_prepare(self)

        return

    def analyze(self):
        my_analyze(self)

        return

    @kernel
    def reset_core(self):
        self.core.reset()

        return


    def run(self):

       
        scan_type = 'power'
        #scan_type = 'frequency'


        if scan_type == 'frequency':

            # Scan frequency
            
            # set microwave power
            self.microwave.freq(self.scan_interval[0] * 1e6) 
            self.microwave.power(self.microwave_power)
            self.microwave.on()
 
            # set frequency range of spectrum analyzer
            self.spectrum_analyzer.set_freq([self.scan_interval[0] * 1e6 - 10.0e6, self.scan_interval[-1] * 1e6 + 10.e6])
            
            # pause to wait till laser settles
            time.sleep(1)

            # counter counts setpoints and averages
            counter = 0
            # loop over setpoints
            for n, nu in enumerate(self.scan_interval):

                self.scheduler.pause()

                self.spectrum_analyzer.set_freq([nu * 1e6 - 10.0e6, nu * 1e6 + 10.e6])
                
                # scan microwave frequency
                self.current_setpoint = nu * 1.0e6

                self.microwave.freq(self.current_setpoint) 

                print("{0:.2f} MHz".format(self.current_setpoint/1e6))

                time.sleep(2)

                # read out trace
                spec = self.spectrum_analyzer.get_trace()

                # save trace
                self.mutate_dataset('set_points',  n, nu)
                self.mutate_dataset('beat_node_fft',  n,  spec)

                print(str(n+1) + ' / ' + str(self.setpoint_count) + ' setpoints')

                print()
                print()

        elif scan_type == 'power':

            # Scan power

            # set microwave power
            self.microwave.on()
 
            # set frequency range of spectrum analyzer
            self.spectrum_analyzer.set_freq([440.0e6, 470.0e6])
            
            self.microwave.freq(460.0e6) 
            
            # pause to wait till laser settles
            time.sleep(1)

            # counter counts setpoints and averages
            counter = 0
            # loop over setpoints
            for n, nu in enumerate(self.scan_interval):

                self.scheduler.pause()

                # scan microwave frequency
                self.current_setpoint = nu

                self.microwave.power(nu) 

                print("{0:.2f} MHz".format(self.current_setpoint))

                time.sleep(1)

                # read out trace
                spec = self.spectrum_analyzer.get_trace()

                # save trace
                self.mutate_dataset('set_points',  n, nu)
                self.mutate_dataset('beat_node_fft',  n,  spec)

                print(str(n+1) + ' / ' + str(self.setpoint_count) + ' setpoints')

                print()
                print()




        # switch off microwave
        self.microwave.off()



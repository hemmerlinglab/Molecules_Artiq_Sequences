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
from scan_functions import scan_parameter


class General_Scan(EnvExperiment):
    
    ##############################################################

    def build(self):

        base_build(self)
        self.sequence_filename = os.path.abspath(__file__)

        pulsed_scan_build(self)

        return

    
    ##############################################################
    
    def prepare(self):

        my_prepare(self)

    
    ##############################################################
    
    def analyze(self):

        my_analyze(self)
    
        return

    
    ##############################################################

    def run(self):

        # check if scan parameter range and scan function is ok
        if self.scan_ok:

            # loop over each scan point
            for my_ind in range(len(self.scan_values)):

                self.scheduler.pause()

                # set the value of the new parameter
                scan_parameter(self, my_ind)





                # counter counts setpoints and averages
                counter = 0
        
                slowing_data = False
        
                # loop over setpoints
                for n, nu in enumerate(self.scan_interval):
        
                    self.scheduler.pause()
        
                    # scan microwave frequency
                    self.current_setpoint = nu * 1.0e6
        
                    self.microwave.freq(self.current_setpoint) 
        
                    for slowing_data in [True, False]:
        
                        # switch on microwave every second data point 
                        if not slowing_data:
                            self.microwave.power(self.microwave_power)
                        else:
                            self.microwave.power(-100)
        
                            # reset counter
                            counter -= self.no_of_averages
        
                        print('{0} / {1} setpoints (slowing_shot = {2}, counter = {3})'.format(n+1, self.setpoint_count, slowing_data, counter))
        
                        time.sleep(0.1)
        
        
                        self.smp_data_avg = {}
                        # loop over averages
                        for i_avg in range(self.no_of_averages):
                            print(str(i_avg+1) + ' / ' + str(self.no_of_averages) + ' averages')
                            self.scheduler.pause()
        
                            repeat_shot = True
                            while repeat_shot:
                                # fires yag and reads voltages
                                fire_and_read(self)
        
                                # readout the data
                                readout_data(self)
        
                                repeat_shot = check_shot(self)
                                
                                if repeat_shot == False:
                                    # upon success add data to dataset
                                    average_data(self, i_avg)
        
                                    update_data(self, counter, n, slowing_data = slowing_data)
        
                                    counter += 1
        
                                time.sleep(self.repetition_time)
        
        
        
                    print()
                    print()







    return





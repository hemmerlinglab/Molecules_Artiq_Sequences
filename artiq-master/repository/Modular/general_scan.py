# use 'artiq-run' command
from artiq.experiment import *

import sys
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")

import numpy as np
import os

# core sequence
from base_sequences import fire_and_read

from my_build_functions   import my_build
from my_prepare_functions import my_prepare
from my_analyze_functions import my_analyze
from scan_functions       import scan_parameter




class General_Scan(EnvExperiment):
    
    ##############################################################

    def build(self):

        my_build(self, which_instruments = ['microwave'])
        self.sequence_filename = os.path.abspath(__file__)

        return

    
    ##############################################################
    
    def prepare(self):

        my_prepare(self)
        
        return

    
    ##############################################################
    
    def analyze(self):

        my_analyze(self)
    
        return


    ##############################################################
    
    def switch_configurations(self, which_configuration):

        # define what happens for the two different sets of configurations
    
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

                # at each iteration, do two runs for the no of averages
                # one with and one without the microwave (or whatever)
                
                # call switch configurations functions
                # then run average

                ## counter counts setpoints and averages
                #counter = 0
        
                #slowing_data = False
        
                ## loop over setpoints
                #for n, nu in enumerate(self.scan_interval):
        
                #    self.scheduler.pause()
        
                #    # scan microwave frequency
                #    self.current_setpoint = nu * 1.0e6
        
                #    self.microwave.freq(self.current_setpoint) 
        
                #    for slowing_data in [True, False]:
        
                #        # switch on microwave every second data point 
                #        if not slowing_data:
                #            self.microwave.power(self.microwave_power)
                #        else:
                #            self.microwave.power(-100)
        
                #            # reset counter
                #            counter -= self.no_of_averages
        
                #        print('{0} / {1} setpoints (slowing_shot = {2}, counter = {3})'.format(n+1, self.setpoint_count, slowing_data, counter))
        
                #        time.sleep(0.1)
        
        
                #        self.smp_data_avg = {}
                #        # loop over averages
                #        for i_avg in range(self.no_of_averages):
                #            print(str(i_avg+1) + ' / ' + str(self.no_of_averages) + ' averages')
                #            self.scheduler.pause()
        
                #            repeat_shot = True
                #            while repeat_shot:
                #                # fires yag and reads voltages
                #                fire_and_read(self)
        
                #                # readout the data
                #                readout_data(self)
        
                #                repeat_shot = check_shot(self)
                #                
                #                if repeat_shot == False:
                #                    # upon success add data to dataset
                #                    average_data(self, i_avg)
        
                #                    update_data(self, counter, n, slowing_data = slowing_data)
        
                #                    counter += 1
        
                #                time.sleep(self.repetition_time)
        
        
        
                #    print()
                #    print()

        return





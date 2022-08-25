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
from rubidium_lines import get_rb_scan_interval

# every Experiment needs a build and a run function
class Scan_Rb_Reference(EnvExperiment):
    
    def build(self):
        base_build(self)

        rubidium_calibration_build(self)

        return

 
    def prepare(self):
        # function is run before the experiment, i.e. before run() is called
            
        #self.scan_interval = np.linspace(self.setpoint_min, self.setpoint_max, self.setpoint_count)
        self.df = 100.0
        self.scan_interval = get_rb_scan_interval(no_of_points = int(self.setpoint_count/6), df = self.df, cnt_freq = self.offset_laser_Hodor*1e12) 
        
        # call the preparation that is in common of all experiments
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



        # init lasers
        set_single_laser(self, 'Hodor', self.offset_laser_Hodor + self.scan_interval[0]/1.0e6, do_switch = True, wait_time = self.relock_wait_time)

        print('relocked')
        
        # pause to wait till laser settles
        time.sleep(1)

        # counter counts setpoints and averages
        counter = 0
        # loop over setpoints
        for n, nu in enumerate(self.scan_interval): 

            self.scheduler.pause()

            self.current_setpoint = self.offset_laser_Hodor + nu/1.0e6

            # set laser frequencies
            set_single_laser(self, 'Hodor', self.current_setpoint, wait_time = self.lock_wait_time)

            print(str(n+1) + ' / ' + str(self.setpoint_count) + ' setpoints')

            if n == 0:
                time.sleep(0.1)
            else:
                time.sleep(2)

            self.smp_data_avg = {}
            # loop over averages
            for i_avg in range(self.scan_count):                
                print(str(i_avg+1) + ' / ' + str(self.scan_count) + ' averages')
                self.scheduler.pause()                
              
                repeat_shot = True
                while repeat_shot:
                    # fires yag and reads voltages
                    read_rubidium(self)

                    # readout the data
                    readout_data(self)

                    repeat_shot = check_shot(self)
                    if repeat_shot == False:                        
                        # upon success add data to dataset
                        average_data(self, first_avg = (i_avg == 0))
                        
                        if i_avg == 0:
                            self.ch1_avg = self.smp_data[self.smp_data_sets['ch1']]
                            self.ch2_avg = self.smp_data[self.smp_data_sets['ch2']]
                        else:
                            self.ch1_avg = (self.ch1_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch1']]) / (i_avg+1.0)
                            self.ch2_avg = (self.ch2_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch2']]) / (i_avg+1.0)

                        update_data(self, counter, n)

                        counter += 1
                    
                    time.sleep(self.repetition_time)

            print()
            print()

        # set laser back to initial point
        set_single_laser(self, 'Hodor', self.offset_laser_Hodor + self.scan_interval[0]/1.0e6, wait_time = self.lock_wait_time)



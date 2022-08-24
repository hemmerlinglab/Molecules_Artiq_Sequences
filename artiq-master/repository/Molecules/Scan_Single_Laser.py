# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime
import os
import time
import csv

from base_functions import *
from base_sequences import *

import sys
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")

from helper_functions import *


# every Experiment needs a build and a run function
class Scan_Single_Laser(EnvExperiment):
    
    def build(self):
        base_build(self)
 
    def prepare(self):
        # function is run before the experiment, i.e. before run() is called
        my_prepare(self)

    def analyze(self):
        my_analyze(self)

    @kernel
    def reset_core(self):
        self.core.reset()


    def run(self):

        # init flow
        set_helium_flow(self.he_flow, wait_time = self.he_flow_wait)

        # init lasers
        set_single_laser(self, 'Hodor', self.offset_laser_Hodor + self.scan_interval[0]/1.0e6, do_switch = True, wait_time = self.relock_wait_time)
        set_single_laser(self, 'Daenerys', self.offset_laser_Daenerys, do_switch = True, wait_time = self.relock_wait_time)

        # pause to wait till laser settles
        time.sleep(1)

        # counter counts setpoints and averages
        counter = 0
        # loop over setpoints
        for n, nu in enumerate(self.scan_interval): 

            self.scheduler.pause()

            self.current_setpoint = self.offset_laser_Hodor + nu/1.0e6

            # set laser frequencies
            # re-lock lasers
            if n % self.relock_laser_steps == 0:
                print('Relocking laser ..')
                set_single_laser(self, 'Daenerys', self.offset_laser_Daenerys, do_switch = True, wait_time = self.relock_wait_time)
                # last laser here should be the one being scanned
                set_single_laser(self, 'Hodor', self.current_setpoint, do_switch = True, wait_time = self.relock_wait_time)
            else:
                set_single_laser(self, 'Hodor', self.current_setpoint, wait_time = self.lock_wait_time)
 

            print(str(n+1) + ' / ' + str(self.setpoint_count) + ' setpoints')

            if n == 0:
                time.sleep(0.1)
            else:
                time.sleep(0.1)

            self.smp_data_avg = {}
            # loop over averages
            for i_avg in range(self.scan_count):                
                print(str(i_avg+1) + ' / ' + str(self.scan_count) + ' averages')
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
                        average_data(self, first_avg = (i_avg == 0))
                        
                        if i_avg == 0:
                            self.ch0_avg = self.smp_data[self.smp_data_sets['ch0']]
                            self.ch2_avg = self.smp_data[self.smp_data_sets['ch2']]
                        else:
                            self.ch0_avg = (self.ch0_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch0']]) / (i_avg+1.0)
                            self.ch2_avg = (self.ch2_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch2']]) / (i_avg+1.0)

                        update_data(self, counter, n)

                        counter += 1
                    
                    time.sleep(self.repetition_time)

            print()
            print()

        # set laser back to initial point
        set_single_laser(self, 'Hodor', self.offset_laser_Hodor + self.scan_interval[0]/1.0e6, wait_time = self.lock_wait_time)
        # switch off Helium flow
        set_helium_flow(0.0, wait_time = 0.0)



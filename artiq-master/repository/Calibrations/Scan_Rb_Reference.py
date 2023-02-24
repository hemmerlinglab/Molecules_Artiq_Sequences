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
        self.sequence_filename = os.path.abspath(__file__)

        rb_calibration_build(self)

        my_setattr(self, 'setpoint_count', NumberValue(default=3,unit='setpoints',scale=1,ndecimals=0,step=1))
        my_setattr(self, 'df', NumberValue(default=50,unit='MHz',scale=1,ndecimals=0,step=1))
        
        my_setattr(self, 'hene_calibration', NumberValue(default=473.6124,unit='THz',scale=1,ndecimals=6,step=1))
        my_setattr(self, 'wavemeter_offset', NumberValue(default=0.0,unit='MHz',scale=1,ndecimals=1,step=1))

        
        return

 
    def prepare(self):
        # function is run before the experiment, i.e. before run() is called

               
        #self.scan_interval = np.linspace(self.setpoint_min, self.setpoint_max, self.setpoint_count)
        self.scan_interval = get_rb_scan_interval(no_of_points = int(self.setpoint_count), df = self.df, cnt_freq = self.offset_laser_Hodor*1e12) 
        self.setpoint_count *= 5 # this needs to be added since we calculate the line intervals here
        

        self.set_dataset('rb_spectrum',     ([0] * self.setpoint_count), broadcast=True)
                
        # call the preparation that is in common of all experiments
        my_prepare(self)

        self.smp_data_sets = {
            'ch0' : 'abs_diff',
            'ch1' : 'absorption_spec',
            'ch2' : 'absorption_spec_reference',
            'ch3' : 'null',
            'ch4' : 'null',
            'ch5' : 'null'
            }

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
        set_single_laser('Hodor', self.offset_laser_Hodor + self.scan_interval[0]/1.0e6, do_switch = True, wait_time = self.relock_wait_time)
        
        # pause to wait till laser settles
        time.sleep(1)

        self.last_setpoint = 0.0

        # counter counts setpoints and averages
        counter = 0
        # loop over setpoints
        for n, nu in enumerate(self.scan_interval): 

            self.scheduler.pause()

            self.current_setpoint = self.offset_laser_Hodor + nu/1.0e6

            # set laser frequencies
            set_single_laser('Hodor', self.current_setpoint, wait_time = self.lock_wait_time)

            # if there is a setpoint jump larger than 200 MHz, then wait for longer
            if np.abs(self.last_setpoint - self.current_setpoint) > 50e-6 and not n == 0:
                print('Sleeping for 3 ...')
                time.sleep(0.3)
            
            self.last_setpoint = self.current_setpoint


            print(str(n+1) + ' / ' + str(self.setpoint_count) + ' setpoints')


            
            self.smp_data_avg = {}
            # loop over averages
            for i_avg in range(self.no_of_averages):                
                print(str(i_avg+1) + ' / ' + str(self.no_of_averages) + ' averages')
                self.scheduler.pause()                
             
                if True:
                    # fires yag and reads voltages
                    read_rubidium(self)

                    # readout the data
                    readout_data(self)

                    if True:
                        # upon success add data to dataset
                        average_data_calibration(self, i_avg)
                        
                        update_data_calibration(self, counter, n, last_point = (i_avg == self.no_of_averages-1))

                        counter += 1
                    
                    time.sleep(self.repetition_time)

            print()
            print()

        # set laser back to initial point
        set_single_laser('Hodor', self.offset_laser_Hodor + self.scan_interval[0]/1.0e6, wait_time = self.lock_wait_time)

        time.sleep(2)
        
        # run fit and then run HeNe calibration

        



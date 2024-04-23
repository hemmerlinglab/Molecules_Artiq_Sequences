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


# every Experiment needs a build and a run function
class Scan_Pulse_Tube_Delay(EnvExperiment):
    
    def build(self):
        base_build(self)
        self.sequence_filename = os.path.abspath(__file__)

        pulsed_scan_build(self) 
        
     
        my_setattr(self, 'delay_min',NumberValue(default=0,unit='ms',scale=1,ndecimals=1,step=1))
        my_setattr(self, 'delay_max',NumberValue(default=700,unit='ms',scale=1,ndecimals=1,step=1))

        return
 
    def prepare(self):
        # function is run before the experiment, i.e. before run() is called
        
        self.scan_interval = np.linspace(self.delay_min, self.delay_max, self.setpoint_count)
 
        self.set_dataset('in_cell_spectrum', ([0] * self.setpoint_count),broadcast=True)
        self.set_dataset('pmt_spectrum',     ([0] * self.setpoint_count),broadcast=True)
        
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

        #set_single_laser(self.scanning_laser, self.offset_laser_Davos, do_switch = True, wait_time = self.relock_wait_time)
        
        # init scanning laser
        if self.scanning_laser == 'Daenerys':
            hlp_frequency_offset = self.offset_laser_Daenerys
        elif self.scanning_laser == 'Hodor':
            hlp_frequency_offset = self.offset_laser_Hodor
        elif self.scanning_laser == 'Davos':
            hlp_frequency_offset = self.offset_laser_Davos

        set_single_laser(self.scanning_laser, hlp_frequency_offset + self.scan_interval[0]/1.0e6, do_switch = True, wait_time = self.relock_wait_time)

        # set Helium flow
        set_helium_flow(self.he_flow, wait_time = self.he_flow_wait)
 
        # counter counts setpoints and averages
        counter = 0
        # loop over setpoints
        for n, my_delay in enumerate(self.scan_interval): 

           
            # set pulse tube delay
            self.current_setpoint = self.pulse_tube_sync_wait
            self.pulse_tube_sync_wait = my_delay


            print(str(n+1) + ' / ' + str(self.setpoint_count) + ' setpoints')

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
                        
                        update_data(self, counter, n)

                        counter += 1
                    
                    time.sleep(self.repetition_time)

            print()
            print()

        set_helium_flow(0.0, wait_time = 0.0)



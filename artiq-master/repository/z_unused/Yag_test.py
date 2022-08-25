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
class Yag_Test(EnvExperiment):

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

        # init lasers
        set_lasers(self, init = True)
       
        # pause to wait till laser settles
        time.sleep(1)

        counter = 0

        n = 0
        # infinite loop
        while True:

            self.smp_data_avg = {}
             
            # loop over averages
            for i_avg in range(self.scan_count):                
                
                print(str(i_avg+1) + ' / ' + str(self.scan_count) + ' averages')
            
                self.scheduler.pause()                
              
                fire_and_read(self)

                # readout the data
                readout_data(self)

                average_data(self,first_avg = (i_avg == 0))
                     
                if i_avg == 0:
                    self.ch0_avg = self.smp_data[self.smp_data_sets['ch0']]
                    self.ch2_avg = self.smp_data[self.smp_data_sets['ch2']]
                else:
                    self.ch0_avg = (self.ch0_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch0']]) / (i_avg+1.0)
                    self.ch2_avg = (self.ch2_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch2']]) / (i_avg+1.0)

                update_data(self,counter, n)

                #counter = (counter + 1)

                time.sleep(self.repetition_time)

            print()
            print()


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
class Dummy_Shots(EnvExperiment):

   
    def build(self):
        base_build(self)
        self.sequence_filename = os.path.abspath(__file__)

        #pulsed_scan_build(self)

        return

    def prepare(self):
        # function is run before the experiment, i.e. before run() is called

        #my_prepare(self)

        return

    def analyze(self):

        return

    @kernel
    def fire_dummy_shot(self):

        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)

        delay(300*us)

        ## shut slowing laser off before anything starts
        #self.ttl8.on()
        #delay(25*ms)

        ### Fire and sample
        with parallel:

            with sequential:
               
                self.ttl11.on()
                
                delay(1*ms)

                self.ttl11.off()

                #delay(20*ms)

                #self.ttl11.on()

                ## starting ramp 2ms before yag
                #delay((0.01 + 30.0 + 0.15 + 0.015 + 0.135 + 0.15 + 0.1 - 2.0)*ms) 
                #
                #self.ttl11.pulse(1*ms) # start cavity scan


        return


    @kernel
    def reset_core(self):
        self.core.reset()

        return


    def run(self):

        k = 0
        while 1:
            self.scheduler.pause()

            print('Fire ' + str(k))
            self.fire_dummy_shot()
            time.sleep(1.0)
            k += 1


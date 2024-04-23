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



# every Experiment needs a build and a run function
class TTL_Test(EnvExperiment):
    def build(self):

        self.config_dict = []
        self.wavemeter_frequencies = []
        
        self.setattr_device('core') # Core Artiq Device (required)
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('ttl5') # uv ccd trigger
        self.setattr_device('ttl8') # slowing shutter
        self.setattr_device('ttl9') # experimental start
        self.setattr_device('ttl7') # uniblitz shutter control

        self.setattr_device('sampler0') # adc voltage sampler
        self.setattr_device('scheduler') # scheduler used

        self.my_setattr('shutter_on',BooleanValue(default=False))
        
    def my_setattr(self, arg, val):
        
        # define the attribute
        self.setattr_argument(arg,val)

        # add each attribute to the config dictionary
        if hasattr(val, 'unit'):
            exec("self.config_dict.append({'par' : arg, 'val' : self." + arg + ", 'unit' : '" + str(val.unit) + "'})")
        else:
            exec("self.config_dict.append({'par' : arg, 'val' : self." + arg + "})")

    ### Script to run on Artiq
    # Basic Schedule:
    # 1) Trigger YAG Flashlamp
    # 2) Wait 150 us
    # 3) Trigger Q Switch
    # 4) In parallel, read off 2 diodes and PMT
    @kernel
    def fire_and_read(self):
        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        self.sampler0.init() # initializes sampler device
        # print('made it here')
        ### Set Channel Gain 
        
        delay(260*us)

        self.ttl8.on()
        delay(500*ms)
        self.ttl8.off()

    def prepare(self):
        # function is run before the experiment, i.e. before run() is called

        # self.core.reset() #### put in @kernel
        self.reset_core()
        # print('made it here')


    def analyze(self):
        # function is run after the experiment, i.e. after run() is called

        return

    @kernel
    def reset_core(self):
        self.core.reset()

    def run(self):

        while True:

            self.scheduler.pause()                
              
            self.fire_and_read()

            time.sleep(1)
            print()
            print()


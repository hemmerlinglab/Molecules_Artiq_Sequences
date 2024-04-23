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
class TrigIn_Test(EnvExperiment):

   
    def build(self):
        base_build(self)
    
        self.setattr_device('ttl3') # uniblitz shutter control
        
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

        a = 0

        ### Fire and sample
        with parallel:

            with sequential:
  
                #if True:
                #for i in range(1000):
                #i = True
                #while i:
                #   # 1us delay, necessary for using trigger, no error given if removed
                #   delay(1000*us)    
    
                #   # sets variable t_edge as time(in MUs) at which first edge is detected
                #   # if no edge is detected, sets t_edge to -1
                #   t_end  = self.ttl3.gate_rising(10*ms)
                #   t_edge = self.ttl3.timestamp_mu(t_end)
    
                #   if t_edge > 0:                       
                #      # runs if an edge has been detected
                #      # set time cursor to position of edge
                #      at_mu(t_edge)                      
                #      delay(5*us)                        
                #      # 5us delay, to prevent underflow
                #      self.ttl11.pulse(5*ms)              
                #      # outputs 5ms pulse on TTL6

                #   #delay(0.25*ms) 
                #   #self.ttl11.pulse(1*ms)
                #   self.ttl3.count(t_end)

                #delay(1*ms)
                while self.ttl3.watch_stay_off():
                    delay(10*us)
                    pass

                delay(10*us)

                delay(400*ms)
                self.ttl11.pulse(10*ms)
                
                if self.ttl3.watch_done():
                    pass
                    #delay(0.25*ms)
                    #self.ttl11.pulse(1*ms)

        #print(t_edge)
        #print(cnt)

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
            #time.sleep(1.0)
            k += 1


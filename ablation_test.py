# use 'artiq-run' command
import sys
import os
import select
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt

# every Experiment needs a build and a run function
class DAQ(EnvExperiment):
    def build(self):
        self.setattr_device('core')
        self.setattr_device('core_dma')
        self.setattr_device('ttl11') # experiment start
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('sampler0')
        self.setattr_argument('scope_count',NumberValue(default=600,ndecimals=0,step=1))
        self.setattr_argument('scan_count',NumberValue(default=1,ndecimals=0,step=1))
        #self.setattr_dataset('scope_read')


    @kernel
    def fire_yag(self):
        self.core.break_realtime()
        self.ttl4.pulse(15*us)
        delay(150*us)
        self.ttl6.pulse(15*us)

    """ Tells it to run at the core device, @ kernel is necessary to run the process entirely in artiq's core
    Notes: 
    - any command that needs to talk to the computer severely slows down (or makes it not work) the process because its not in artiq's processer
    - normal python commands such as print and plotting figures slows the kernel, or will make it not work"""
    @kernel
    def read_diode(self):
        self.core.break_realtime()
        self.sampler0.init()
        
        """ 
         This function sets the gain for each sampler channel according manual
         * i iterates over 8 channels
         * gain setting of 0 is 1
         * gain is 10^(input setting is), which is the second number in the .set_gain_mu
         --> currently has a gain of 1 """    
        for i in range(8):
            self.sampler0.set_gain_mu(i,0)
        
        # initilization, sets up the array of zeros of values to be replaced
        data = [0]*self.scope_count
        smp = [0]*8 # array of numbers coming from each sampler port
        # Takes the data from the scope
        # actually doing the sampling
        #elap = self.core.get_rtio_counter_mu()
        for j in range(self.scope_count):
            delay(5.0*us)
            self.sampler0.sample_mu(smp) # reads out into smp which takes data from all 8 ports
            data[j] = smp[0] # replaces the value at specified data[j] with the updated scalar from smp[0] (channel 0 of the sampler ports)  
            
             # needed to prevent underflow errors
        #elap_t = self.core.mu_to_seconds(self.core.get_rtio_counter_mu() - elap)
        index = range(self.scope_count)
        self.mutate_dataset('scope_read',index,data)
        #print('Elapsed time:',elap_t)

    def run(self):
        self.core.reset()
        x = np.arange(self.scope_count)
        self.set_dataset('scope_read',np.full(self.scope_count,np.nan))
        for i in range(self.scan_count):
            input('Press ENTER for Run {}/{}'.format(i+1,self.scan_count))
            self.fire_yag()
            self.read_diode()
            print('Run {}/{} Completed'.format(i+1,self.scan_count))

        vals = self.get_dataset('scope_read')
        volts = []
        for v in vals:
            volts.append(splr.adc_mu_to_volt(v))
        #print(volts)
        f_name = 'test2.txt'
        f_out = open(f_name,'w')
        for v in volts:
            f_out.write(str(v)+' ')
        f_out.close()



        



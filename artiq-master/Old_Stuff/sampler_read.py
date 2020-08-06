# use 'artiq-run' command
# works with the GUI

import sys
import os
import select
from artiq.experiment import *
from artiq.coredevice.ad9910 import AD9910
from artiq.coredevice.ad53xx import AD53xx
import time
import numpy as np

def print_underflow():
    print('RTIO underflow occured')

class DAQ(EnvExperiment):
    def build(self):
        self.setattr_device('core')
        self.setattr_device('ttl11') # experiment start
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('sampler0')
        #self.setattr_argument("count",NumberValue(default=10,ndecimals=0,step=1))
        #self.name = 
        #self.setattr_dataset()

    @kernel
    def get_sampler_voltages(self,sampler,cb):
        self.core.break_realtime()
        #print('loc1')
        sampler.init()
        #print('loc2')
        delay(10*ms)
        sampler.set_gain_mu(0,0)
        delay(10*ms)
        #for i in range(8):
        #    sampler.set_gain_mu(i,0)
        #    delay(100*us)
        #print('loc3')
        #smps = [[0.0]]*8
        smp = [0.0]*8
        #for i in range(10):
        sampler.sample(smp)
            #smps[i] = smp
        delay(100*us)
            
        #print('loc4')
        cb(smp)

        #print('loc5')

    def test_sampler(self):
        voltages = []
        #print("asd")
        def setv(x):                        
            nonlocal voltages
            voltages = x                        
        #print("asd2")
        self.get_sampler_voltages(self.sampler0,setv)
        #print("asd3")
        #or voltage in voltages:
        #    print(voltage)
        #print(voltages)
        return(voltages)

    #@kernel
    def run(self):
        self.core.reset()
        volt = self.test_sampler()
        print(volt)
        #self.set_dataset('voltages',np.full(self.count,np.nan),broadcast=True)
        #for i in range(self.count):
        #  self.mutate_dataset('voltages',i,self.test_sampler()[0])
        
        #self.write_daq()
        #print(data)
        #except RTIOUnderflow:
        #    print_underflow()

# use 'artiq-run' command
import sys
import os
import select
from artiq.experiment import *
from artiq.coredevice.ad9910 import AD9910
from artiq.coredevice.ad53xx import AD53xx

""" Kayla's version with notes!
    Notes on possible problems: 
    1. there is no init function in the class, no initialization which is     probably one of its problems 
    2. On page 48 of the manual, it says that user- written experiments should derive from the artiq.language.environment.EnvExperiment sub class, should this be imported or does the EnvExperiment class here work?
    Questions:
    1. When is a kernel needed, this is not clear
    """

def print_underflow():
    print('RTIO underflow occured')

class DAQ(EnvExperiment):
    def build(self):
        self.setattr_device('core')
        self.setattr_device('ttl11') # experiment start
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('sampler0')

    @kernel
    def get_sampler_voltages(self,sampler,cb):
        self.core.break_realtime()
        #print('loc1')
        sampler.init()
        #print('loc2')
        delay(5*ms)
        sampler.set_gain_mu(0,0)
        delay(5*ms)
        #for i in range(8):
        #    sampler.set_gain_mu(i,0)
        #    delay(100*us)
        #print('loc3')
        smps = [[0.0]]*8
        smp = [0.0]*8
        for i in range(10):
            sampler.sample(smp)
            smps[i] = smp
            delay(100*us)
            
        #print('loc4')
        cb(smps)

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
        data = []
        n = 100
        for i in range(n):
            newdata = self.test_sampler()
            print('Sample: {}/{}'.format(i,n),end='\r')
            data.append(newdata[0])
        
        #self.write_daq()
        print(data)
        #except RTIOUnderflow:
        #    print_underflow()

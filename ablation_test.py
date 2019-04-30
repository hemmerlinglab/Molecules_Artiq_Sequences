# use 'artiq-run' command
import sys
import os
import select
from artiq.experiment import *
from artiq.coredevice.ad9910 import AD9910

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
        sampler.init()
        delay(5*ms)
        for i in range(8):
            sampler.set_gain_mu(i,0)
            delay(100*us)
        smp = [0.0]*8
        sampler.sample(smp)
        cb(smp)

    def test_sampler(self):
        voltages = []
        print("asd")
        def setv(x):                        
            nonlocal voltages
            voltages = x                        
        print("asd2")
        self.get_sampler_voltages(self.sampler0,setv)
        print("asd3")
        for voltage in voltages:
            print(voltage)
        #print("asd")

    @kernel
    def run(self):
        self.core.reset()
        
        try:            
            while True:
                with parallel:
                    with sequential:
                        #self.ttl11.pulse(5*us)
                        self.ttl4.pulse(5*us)
                        delay(30*us)
                        self.ttl4.pulse(5*us)
                        delay(100*us)
                    with sequential:
                        delay(35*us)
                        self.ttl6.pulse(5*us)
                        delay(20*us)
                        self.ttl6.pulse(5*us)

                        self.test_sampler()

                        #print("Start experiment")            
                        delay(1000*ms)

        except RTIOUnderflow:
            print_underflow()

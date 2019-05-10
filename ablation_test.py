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

    @kernel
    def read_diode(self):
        self.core.break_realtime()
        self.sampler0.init()

        for i in range(8):
            self.sampler0.set_gain_mu(i,0)

        data = [0]*self.scope_count
        smp = [0]*8
        
        for j in range(self.scope_count):
            self.sampler0.sample_mu(smp)
            data[j] = smp[0]
            delay(5*us)

        index = range(self.scope_count)
        self.mutate_dataset('scope_read',index,data)

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
        print(volts)


        



# use 'artiq-run' command
import sys
import os
import select
from artiq.experiment import *
import datetime
import time
import numpy as np

class DAQ(EnvExperiment):
    def build(self):
        self.setattr_device('core')
        self.setattr_device('core_dma')
        self.setattr_device('ttl11') # experiment start
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('sampler0')
        self.setattr_argument('scope_count',NumberValue(default=100,ndecimals=0,step=1))
        self.setattr_argument('scan_count',NumberValue(default=3,ndecimals=0,step=1))
        #self.setattr_dataset('scope_read')


    @kernel
    def fire_yag(self):
        self.core.break_realtime()
        self.ttl4.pulse(15*us)
        delay(150*us)
        self.ttl6.pulse(15*us)


    @kernel
    def read_diode(self,read_n):
        self.core.break_realtime()
        
        data = [0.0]*self.scope_count
        smp = [0.0]*8
        for dt in range(self.scope_count):
            self.sampler0.sample_mu(smp)
        #self.mutate_dataset('scope_read',(read_n,dt),smp[0])


    def run(self):
        self.core.reset()
        self.sampler0.init()
        self.sampler0.set_gain_mu(0,0)
        self.set_dataset('scope_read',np.full((self.scan_count,self.scope_count),np.nan))
        for i in range(self.scan_count):
            input('Press ENTER for Run {}/{}'.format(i+1,self.scan_count))
            self.fire_yag()
            self.read_diode(i)
            print('Run {}/{} Completed'.format(i+1,self.scan_count))





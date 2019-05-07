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
        self.setattr_argument('scope_count',NumberValue(default=20,ndecimals=0,step=1))
        self.setattr_argument('scan_count',NumberValue(default=3,ndecimals=0,step=1))
        #self.setattr_dataset('scope_read')


    @kernel
    def fire_yag(self):
        self.core.break_realtime()
        self.ttl4.pulse(15*us)
        delay(150*us)
        self.ttl6.pulse(15*us)

    @kernel
    def read_diode(self, cb):
        self.core.break_realtime()
        self.sampler0.init()

        for i in range(8):
            self.sampler0.set_gain_mu(i,0)

        smp = [0]*8
        
        self.sampler0.sample_mu(smp)

        cb(smp)
        #return smp




    #@kernel
    def sample_loop(self,read_n):
        data = []
        vol = []

        voltages = []
        def setv(x):
            nonlocal voltages
            voltages = x
        for k in range(self.scope_count):
            self.read_diode(setv)

            data.append(voltages[0])

        for j in range(self.scope_count):
            vol.append(splr.adc_mu_to_volt(data[j]))

        return vol


    def run(self):
        self.core.reset()
        lore = []
        x = np.arange(self.scope_count)
        for i in range(self.scan_count):
            input('Press ENTER for Run {}/{}'.format(i+1,self.scan_count))
            self.fire_yag()
            vals = self.sample_loop(i)
            lore.append(vals)
            print('Run {}/{} Completed'.format(i+1,self.scan_count))
            print('>>> Data: ',vals)
            fig = plt.figure()
            fig, ax = plt.subplots()
            ax.plot(x,vals)
            plt.show()
        print('>>> Lore: ',lore)


        



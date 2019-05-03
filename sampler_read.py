# use 'artiq-run' command
import sys
import os
import select
from artiq.experiment import *
from artiq.coredevice.ad9910 import AD9910
from artiq.coredevice.ad53xx import AD53xx
import time
import datetime
import numpy as np

def print_underflow():
    print('RTIO underflow occured')


""" Notes on possible problems: 
    1. there is no init function in the class, no initialization which is probably one of its problems """


class DAQ(EnvExperiment):
    def build(self):
        self.setattr_device('core')
        self.setattr_device('core_dma')
        self.setattr_device('ttl11') # experiment start
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('sampler0')
        self.setattr_argument('scope_count',NumberValue(default=20,ndecimals=0,step=1))
        #self.setattr_dataset('')

    @kernel
    def get_sampler_voltages(self,sampler,cb):
        self.core.break_realtime()
        #print('loc1')
        sampler.init()
        #print('loc2')
        #delay(5*ms)
        sampler.set_gain_mu(0,0)
        #delay(5*ms)
        #for i in range(8):
        #    sampler.set_gain_mu(i,0)
        #    delay(100*us)
        #print('loc3')
        #smps = [[0.0]]*8
        smp = [0.0]*8
        #for i in range(10):
        sampler.sample(smp)
        #    smps[i] = smp
        #delay(100*us)
            
        #print('loc4')
        cb(smp)

        #print('loc5')

    def test_sampler(self,dataname):
        self.set_dataset(dataname,np.full(self.scope_count,np.nan))
        voltages = []
        #print("asd")
        def setv(x):                        
            nonlocal voltages
            voltages = x                        
        #print("asd2")
        t1 = time.time()
        # print('Now 1: 0')
        # for i in range(self.scope_count):
        #     self.get_sampler_voltages(self.sampler0,setv)
        #     self.mutate_dataset(dataname,i,voltages[0])
        # print('Now 2:',time.time()-t1)
        #print("asd3")
        #for voltage in voltages:
        #    print(voltage)
        #print(voltages)
        #return(self.get_dataset())

    @kernel
    def record(self):
        pass




    #@kernel
    def run(self):
        self.core.reset()
        self.set_dataset('data1',np.full(self.scope_count,np.nan))
        self.record()
        play_handle = self.core_dma.get_handle('sampling')
        self.core.break_realtime()
        while True:
            #input('Press ENTER:')
            self.core_dma.playback_handle(play_handle)


        #ahora = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        #self.test_sampler(ahora)
        #data = self.get_dataset(ahora)
        #print('run finished')




        # for i in range(n):
        #     newdata = self.test_sampler()
        #     print('Sample: {}/{}'.format(i,n),end='\r')
        #     data.append(newdata[0])
        
        # self.write_daq()
        # print(data)
        # except RTIOUnderflow:
        #    print_underflow()

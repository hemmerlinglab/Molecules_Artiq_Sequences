# use 'artiq-run' command
import sys
import os
from artiq.experiment import *
from artiq.coredevice.sampler import * # used for ADC for sampler


""" Kayla's version with notes!
    Current problems:
    1. sampler reads too slow, not exactly sure how John knows this
    
    
    Answered Questions/ Notes:
    1. port labeling, need to make sure to define the port or device being used in the build function, here the port we are using is 'sampler0'

    Questions:
    1. When is a kernel needed, this is not clear
    
    ** Read and practice the commands for the sampler voltages section of the artiq manual
    ** Core Functionality --> when do we need to have core defined in the device section? is this always?
    """

class DAQ(EnvExperiment):
    def build(self):
        self.setattr_device('core')
        self.setattr_device('sampler0')

    @kernel
    def get_sampler_voltages(self,sampler,cb):
        self.core.break_realtime()
        sampler.init()
        sampler.set_gain_mu(0,0)
        smp = [0.0]*8
        sampler.sample(smp)
        cb(smp)
        return smp

    def run(self):
        self.core.reset()
        for i in range(len(get_sampler_voltages())):
            print(data[i])


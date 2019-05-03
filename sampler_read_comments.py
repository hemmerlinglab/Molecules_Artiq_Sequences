# use 'artiq-run' command
import sys
import os
from artiq.experiment import *
from artiq.coredevice.sampler import * # used for ADC for sampler


""" Kayla's version with notes!
    Plan:
    1. add the get_sampler voltages function --> gets the voltage from artiq hardware
    ** Need to figure out port labeling
    2. print the sampler voltages in the run function
    
    Notes on possible problems: 
    1. there is no init function in the class, no initialization which is     probably one of its problems 
    2. On page 48 of the manual, it says that user- written experiments should derive from the artiq.language.environment.EnvExperiment sub class, should this be imported or does the EnvExperiment class here work?
    
    Questions:
    1. When is a kernel needed, this is not clear
    """

class DAQ(EnvExperiment):
    def build(self):
        self.setattr_device('core')
        self.setattr_device('sampler0')

    #def get_sampler_voltages():
        # this is the function that needs to work
        # include the port to read from, just use photodiode, get an array of zeros
        # return an array of sampler voltages
    
    def run(self):
        self.core.reset()
        data = [0,0,0] # will be replaced with the sampler voltages read from function
        for i in range(len(data)):
            print(data[i])


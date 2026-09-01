# use 'artiq-run' command
from artiq.experiment import *

import os
import sys
import time
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")

import numpy as np
from my_build_functions   import my_build
from my_prepare_functions import my_prepare
from my_analyze_functions import my_analyze
from my_run_functions     import my_run_slowing

from base_dds_sequences   import dds_on, dds_off

from my_build_functions   import my_setattr

###################################################################################
# Experiment
###################################################################################

class Slowing_Scan(EnvExperiment):


    ##############################################################

    def build(self):

        my_build(self, which_instruments = ['BK4053'])#, 'frequency_comb']) #, 'scope_transfer_cavity'])
        #my_build(self, which_instruments = ['frequency_comb'])
        self.sequence_filename = os.path.abspath(__file__)

        return


    ##############################################################
    
    def prepare(self):

        self.configurations = [0]
        
        self.configuration_descriptions = ['Slowing on', 'Slowing off']

        my_prepare(self)
                
        return

    
    ##############################################################
    
    def analyze(self):

        my_analyze(self)
    
        return


    ##############################################################
    
    def switch_configurations(self):

        # define what happens for the two different sets of configurations
        
        # add a note in config to say what happened

        if self.current_configuration == 0:
            # slowing laser on
            dds_on(self)
            self.bk4053.on(channel = 1) # AOM pulsed on

        elif self.current_configuration == 1:
            # slowing laser off
            dds_off(self)
            self.bk4053.off(channel = 1) # AOM always off

        else:
            print('Configuration not defined.')
            asd
        
        return


    ##############################################################

    def run(self):

        my_run_slowing(self)

        return





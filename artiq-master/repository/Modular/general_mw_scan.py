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
from my_run_functions     import my_run

from microwave_windfreak import Microwave


###################################################################################
# Experiment
###################################################################################

class General_MW_Scan(EnvExperiment):


    ##############################################################

    def build(self):

        my_build(self, which_instruments = ['microwave'])
        #my_build(self, which_instruments = [])
        self.sequence_filename = os.path.abspath(__file__)

        return


    ##############################################################
    
    def prepare(self):

        self.configurations = [0]
        
        self.configuration_descriptions = ['Microwave on', 'Microwave off']

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
            # Microwave on
            
            self.microwave.on()
            
        elif self.current_configuration == 1:
            # Microwave off
            
            self.microwave.off()
            
        else:
            print('Configuration not defined.')
            asd
        
        return


    ##############################################################

    def run(self):

        my_run(self)

        return





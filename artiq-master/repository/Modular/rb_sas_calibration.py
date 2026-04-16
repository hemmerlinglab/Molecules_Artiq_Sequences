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
from my_run_functions     import my_run_no_yag


###################################################################################
# Experiment
###################################################################################

class Rubidium_SAS_Spectroscopy(EnvExperiment):


    def update_config(self, par, val):

        ind_config = self.config_dict_no[par]

        self.config_dict[ind_config]['val'] = val

        return


    ##############################################################

    def build(self):

        my_build(self, which_instruments = [])
        self.sequence_filename = os.path.abspath(__file__)
       
        # override parameters
        self.scanning_parameter = 'offset_laser_Davos'

        self.update_config('scanning_parameter', 'offset_laser_Davos')

        self.scanning_laser = 'Davos'

        self.update_config('scanning_laser', 'Davos')

        # R-87 F=2 -> F'=2
        aom_freq = 85e6
        self.offset_laser_Davos = (384.227849e12 + aom_freq)/1e12 # THz

        self.update_config('offset_laser_Davos', self.offset_laser_Davos)

        self.which_scanning_laser = 2

        self.setpoint_count = 100 + 40
        self.update_config('setpoint_count', self.setpoint_count)

        self.he_flow = 0.0
        self.update_config('he_flow', self.he_flow)

        return


    ##############################################################
    
    def prepare(self):

        self.configurations = [0]

        self.configuration_descriptions = ['Laser on']

        # override some attributes

        my_prepare(self)

        self.scan_values = np.linspace(-40, 360, 100)

        self.scan_values = np.append(self.scan_values, np.linspace(1260, 1430, 40))

        self.set_dataset('freqs',      (self.scan_values),broadcast=True)        

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
            # laser on
            pass
            
        else:
            print('Configuration not defined.')
            asd
        
        return


    ##############################################################

    def run(self):

        my_run_no_yag(self)

        return





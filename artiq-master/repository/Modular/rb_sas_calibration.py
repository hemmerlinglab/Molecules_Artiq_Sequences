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
 
        self.offset_laser_Davos = 384.227990
        self.update_config('offset_laser_Davos', 384.227990)
        
        self.which_scanning_laser = 1

        self.setpoint_count = 160
        self.update_config('setpoint_count', 160)

        self.no_of_averages = 2
        self.update_config('no_of_averages', 2)

        self.he_flow = 0.0
        self.update_config('he_flow', 0.0)



        return


    ##############################################################
    
    def prepare(self):

        self.configurations = [0]
        
        self.configuration_descriptions = ['Laser on']

    
        # override some attributes
        
        #self.scanning_parameter = 'offset_laser_Davos'
        #self.scanning_laser     = 'Davos'
        #self.which_scanning_laser  = 1
        #
        #self.offset_laser_Davos = 384.22799
       
        #self.no_of_averages = 1
        #self.setpoint_count = 80
        #self.setpoint_count = 8
        
        my_prepare(self)
        
        self.scan_values = np.linspace(-100, 300, 80)

        self.scan_values = np.append(self.scan_values, np.linspace(1150, 1400, 80))
 
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





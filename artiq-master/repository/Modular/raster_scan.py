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
from my_run_functions     import my_run_raster

from my_build_functions   import my_setattr


###################################################################################
# Experiment
###################################################################################

class Raster_Scan(EnvExperiment):


    ##############################################################

    def build(self):

        my_build(self, which_instruments = [], raster_scan = True)
        self.sequence_filename = os.path.abspath(__file__)
       
        return


    ##############################################################
    
    def prepare(self):

        self.configurations = [0]
        
        self.configuration_descriptions = ['Laser on']


        self.scan_x_interval = np.linspace(self.min_x, self.max_x, self.steps_x)
        self.scan_y_interval = np.linspace(self.min_y, self.max_y, self.steps_y)

        self.setpoint_count = len(self.scan_x_interval) * len(self.scan_y_interval)

        target_img_incell = [[0] * len(self.scan_y_interval)] * len(self.scan_x_interval) 
        self.set_dataset('target_img_incell',(np.array(target_img_incell)),broadcast=True)

        (mesh_X, mesh_Y) = np.meshgrid(self.scan_x_interval, self.scan_y_interval)
        mesh_X = mesh_X.flatten()
        mesh_Y = mesh_Y.flatten()

        self.set_dataset('posx',      (mesh_X),broadcast=True)
        self.set_dataset('posy',      (mesh_Y),broadcast=True)

        my_prepare(self, data_to_save = 
                         [
                            {'var' : 'set_points',             'name' : 'set_points'},
                            {'var' : 'act_freqs',              'name' : 'actual frequencies (wavemeter)'},
                            {'var' : 'freqs',                  'name' : 'freqs'},
                            {'var' : 'times',                  'name' : 'times'},
                            {'var' : 'frequency_comb_frep',    'name' : 'Repetition frequency of comb'},
                            {'var' : 'EOM_frequency',          'name' : 'EOM_frequency'},
                            {'var' : 'beat_node_fft',          'name' : 'FFT of beat node with comb'},
                            {'var' : 'posx',                   'name' : 'posx'},
                            {'var' : 'posy',                   'name' : 'posy'},
                            {'var' : 'target_img_incell',      'name' : 'img'}
                         ]
                )
                
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
            pass
            
        else:
            print('Configuration not defined.')
            asd
        
        return


    ##############################################################

    def run(self):

        my_run_raster(self)

        return





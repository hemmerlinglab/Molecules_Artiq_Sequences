# use 'artiq-run' command
from artiq.experiment import *

import sys
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")

import numpy as np
import os
import time

# core sequence
from base_sequences           import fire_and_read
from process_and_readout_data import readout_data, check_shot, average_data, update_data_sets

from my_build_functions   import my_build
from my_prepare_functions import my_prepare
from my_analyze_functions import my_analyze
from scan_functions       import scan_parameter




class General_Scan(EnvExperiment):


    ##############################################################

    def build(self):

        my_build(self, which_instruments = ['microwave'])
        self.sequence_filename = os.path.abspath(__file__)

        return


    ##############################################################
    
    def prepare(self):

        self.configurations = [0, 1]
        
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
            print('now in {0}'.format(self.current_configuration))
        elif self.current_configuration == 1:
            print('now in {0}'.format(self.current_configuration))
        else:
            print('Configuration not defined.')
            asd

        return


    ##############################################################

    def run(self):


        # check if scan parameter range and scan function is ok
        if self.scan_ok:
            
            counter = 0

            # loop over each scan point
            for my_ind in range(len(self.scan_values)):

                self.scheduler.pause()

                # set the value of the new parameter
                scan_parameter(self, my_ind)

                # call switch configurations functions
                # then run average

                
                ###########################################################
                # Loop over averages for each set point
                ###########################################################

                for i_avg in range(self.no_of_averages):
        
                    print('    Averages: {0:2.0f}/{1:2.0f}'.format(i_avg, self.no_of_averages))

                    for c_ind in self.configurations:
                        
                        self.scheduler.pause()
                        
                        self.current_configuration = c_ind

                        print('          Configuration: {0}'.format(self.current_configuration))

                        self.switch_configurations()

                        self.smp_data_avg = {}
        
                        repeat_shot = True
                        while repeat_shot:
                           
                           #######################################
                           # Fires yag and reads voltages
                           #######################################
                           
                           fire_and_read(self)
        
                           #######################################
                           # Readout data and process it
                           #######################################

                           readout_data(self)
        
                           #######################################
                           # Check if shot is ok and repeat if not
                           #######################################

                           repeat_shot = check_shot(self)
                           if repeat_shot == False:
                               
                               # upon success add data to dataset
                               average_data(self, i_avg)
        
                               update_data_sets(self, counter, my_ind)

                               # counter needs to be reset to not count configurations double
                               counter += 1
        
                        time.sleep(self.repetition_time)


                print()
                print()

        return





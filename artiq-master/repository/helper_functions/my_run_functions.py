from artiq.experiment import *
import numpy as np
import os
import time


# core sequence
from base_sequences           import fire_and_read, no_fire_and_read
from process_and_readout_data import readout_data, check_shot, average_data, update_data_sets, update_data_sets_raster

from scan_functions          import scan_parameter
from my_instrument_functions import move_yag_mirror

###################################################################################

def my_run(self):

    # check if scan parameter range and scan function is ok
    if self.scan_ok:
        
        counter = 0
    
        ###########################################################
        # Loop over set points
        ###########################################################
    
        for my_ind in range(len(self.scan_values)):
    
            self.scheduler.pause()
    
            # set the value of the new parameter
            scan_parameter(self, my_ind)
    
            ###########################################################
            # Loop over averages for each set point
            ###########################################################
    
            for i_avg in range(self.no_of_averages):
    
                print('    Averages: {0:2.0f}/{1:2.0f}'.format(i_avg + 1, self.no_of_averages))
            
                # Loop over all configurations
    
                for self.current_configuration in self.configurations:
                    
                    self.switch_configurations()
 
                    # Wait for the repetition time
                    # This step is in the beginning to allow the configuration switch to happen
                    time.sleep(self.repetition_time)
                   
                    self.scheduler.pause()
                    
                    print('          Configuration: {0}'.format(self.configuration_descriptions[self.current_configuration]))
                    
                    #time.sleep(1)

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
    
            print()
            print()


###################################################################################

def my_run_raster(self):

    # check if scan parameter range and scan function is ok
    if self.scan_ok:
        
        counter = 0
    
        ###########################################################
        # Loop over set points
        ###########################################################
    
        for nx, xpos in enumerate(self.scan_x_interval): 
           for ny, ypos in enumerate(self.scan_y_interval): 
    
            self.scheduler.pause()
    
            # set the value of the new parameter
            # allow for some time at the edges
            if (nx == 0) or (ny == 0):
                move_yag_mirror(xpos, ypos, wait_time = 1)
            else:
                move_yag_mirror(xpos, ypos)
            
            # give the first initial point more time
            if (nx == 0) and (ny == 0):
                time.sleep(2)

            print("Raster point: {0}/{1}".format(counter, self.no_of_averages * len(self.scan_x_interval) * len(self.scan_y_interval)))
            
            ###########################################################
            # Loop over averages for each set point
            ###########################################################
    
            for i_avg in range(self.no_of_averages):
    
                print('    Averages: {0:2.0f}/{1:2.0f}'.format(i_avg + 1, self.no_of_averages))
            
                # Loop over all configurations
    
                for self.current_configuration in self.configurations:
                    
                    self.switch_configurations()
 
                    # Wait for the repetition time
                    # This step is in the beginning to allow the configuration switch to happen
                    time.sleep(self.repetition_time)
                   
                    self.scheduler.pause()
                    
                    print('          Configuration: {0}'.format(self.configuration_descriptions[self.current_configuration]))
                    
                    #time.sleep(1)

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
    
                           update_data_sets_raster(self, counter, nx, ny)
    
                    
                # counter needs to be reset to not count configurations double
                counter += 1
    
            print()
            print()


###################################################################################

def my_run_no_yag(self):

    # check if scan parameter range and scan function is ok
    if self.scan_ok:
        
        counter = 0
    
        ###########################################################
        # Loop over set points
        ###########################################################
    
        for my_ind in range(len(self.scan_values)):
    
            self.scheduler.pause()
    
            # set the value of the new parameter
            scan_parameter(self, my_ind)
    
            ###########################################################
            # Loop over averages for each set point
            ###########################################################
    
            for i_avg in range(self.no_of_averages):
    
                print('    Averages: {0:2.0f}/{1:2.0f}'.format(i_avg + 1, self.no_of_averages))
            
                # Loop over all configurations
    
                for self.current_configuration in self.configurations:
                    
                    self.switch_configurations()
 
                    # Wait for the repetition time
                    # This step is in the beginning to allow the configuration switch to happen
                    time.sleep(self.repetition_time)
                   
                    self.scheduler.pause()
                    
                    print('          Configuration: {0}'.format(self.configuration_descriptions[self.current_configuration]))
                    
                    #time.sleep(1)

                    self.smp_data_avg = {}
    
                    repeat_shot = True
                    
                    while repeat_shot:
                       
                       #######################################
                       # Fires yag and reads voltages
                       #######################################
                       
                       no_fire_and_read(self)
    
                       #######################################
                       # Readout data and process it
                       #######################################
    
                       readout_data(self)
    
                       #######################################
                       # Check if shot is ok and repeat if not
                       #######################################
    
                       repeat_shot = False
                       if repeat_shot == False:
                           
                           # upon success add data to dataset
                           average_data(self, i_avg)
    
                           update_data_sets(self, counter, my_ind)
    
                    
                # counter needs to be reset to not count configurations double
                counter += 1
    
            print()
            print()



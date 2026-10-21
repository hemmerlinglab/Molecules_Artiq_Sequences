from artiq.experiment import *
from artiq.coredevice import ad9910

import numpy as np
import os
import time

# core sequence
from base_sequences           import * 
from base_dds_sequences       import prg_freq_ramp, dds_off
from process_and_readout_data import readout_data, check_shot, average_data, update_data_sets, update_data_sets_raster

from scan_functions           import scan_parameter
from my_instrument_functions  import move_yag_mirror, prepare_dds_ramp, set_single_laser, prepare_bk4053, program_siglent_ramp

###################################################################################

def my_run_slowing_Siglent(self):

    SIGLENT_MAX  = 500.0
    AMP_MIN  =  10.0
    FREQ_AOM =  85.0

    WAVELENGTH = 400e-9

    BEAM_ANGLE = 135.0 * np.pi/180.0

    # check if scan parameter range and scan function is ok
    if self.scan_ok:
        
        counter = 0
   
        ###########################################################
        # Loop over set points
        ###########################################################    

        for my_ind in range(len(self.scan_values)):
    
            self.scan_index = my_ind

            self.scheduler.pause()
  


            ###########################################
            # Distinguish scanning cases
            ###########################################
            
            if self.scanning_parameter == 'velocity':
            
                # Case: Scanning the velocity

                self.velocity = self.scan_values[my_ind] # in m/s

                # calculate velocity shift in the blue
                self.current_velocity_frequency_shift = self.velocity/WAVELENGTH * np.cos(BEAM_ANGLE) # in Hz


            else:
                
                # Case: Scanning anything else
                
                self.current_velocity_frequency_shift = self.velocity/WAVELENGTH * np.cos(BEAM_ANGLE) # in Hz
                
                freq_val = 0.5 * (self.current_velocity_frequency_shift)/1e6 # in MHz

                frequency = self.offset_laser_Hodor + freq_val/1.0e6 # in THz

                set_single_laser('Hodor', frequency, do_switch = False, wait_time = self.relock_wait_time)


            ###########################################
            # set the value of the new parameter
            ###########################################
            
            scan_parameter(self, my_ind)
 

            #########################################
            # Prepare BK 4053
            #########################################
           
            # update the pulse of the BK 4053
            prepare_bk4053(self)


            #########################################
            # Programming of ramp
            #########################################
           
            # high frequency
            Omega_b_start = FREQ_AOM + (1/WAVELENGTH * self.slowing_vel_high + self.current_velocity_frequency_shift)/1.0e6

            # low frequency            
            Omega_a_stop  = FREQ_AOM + (1/WAVELENGTH * self.slowing_vel_low + self.current_velocity_frequency_shift)/1.0e6
            
            print(f"slowing start in frequency {Omega_b_start}")
            print(f"slowing stop in frequency {Omega_a_stop}")


            if Omega_b_start > SIGLENT_MAX:
                print('Error. Omega_b too high. {0:.1f}/{1:.1f}'.format(Omega_b_start, Omega_a_stop))
                Omega_b_start = 10.0
            if Omega_a_stop < AMP_MIN:
                print('Error. Omega_a too low. {0:.1f}/{1:.1f}'.format(Omega_b_start, Omega_a_stop))
                Omega_a_stop = 10.0

            
            program_siglent_ramp(self,
                    start = Omega_b_start, 
                    stop = Omega_a_stop, 
                    duration = self.slowing_laser_duration * ms
                    )
          
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
                    
                    # Dictionary to display averaged data
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
            
    return


###################################################################################

def my_run_slowing_DDS(self):

    DDS_MAX  = 400.0
    DDS_MIN  =  10.0
    FREQ_AOM =  85.0

    WAVELENGTH = 400e-9

    BEAM_ANGLE = 135.0 * np.pi/180.0

    # check if scan parameter range and scan function is ok
    if self.scan_ok:
        
        counter = 0
   
        ###########################################################
        # Loop over set points
        ###########################################################    

        for my_ind in range(len(self.scan_values)):
    
            self.scan_index = my_ind

            self.scheduler.pause()
  


            ###########################################
            # Distinguish scanning cases
            ###########################################
            
            if self.scanning_parameter == 'velocity':
            
                # Case: Scanning the velocity

                self.velocity = self.scan_values[my_ind] # in m/s

                # calculate velocity shift in the blue
                self.current_velocity_frequency_shift = self.velocity/WAVELENGTH * np.cos(BEAM_ANGLE) # in Hz


            else:
                
                # Case: Scanning anything else
                
                self.current_velocity_frequency_shift = self.velocity/WAVELENGTH * np.cos(BEAM_ANGLE) # in Hz
                
                freq_val = 0.5 * (self.current_velocity_frequency_shift)/1e6 # in MHz

                frequency = self.offset_laser_Hodor + freq_val/1.0e6 # in THz

                set_single_laser('Hodor', frequency, do_switch = False, wait_time = self.relock_wait_time)


            ###########################################
            # set the value of the new parameter
            ###########################################
            
            scan_parameter(self, my_ind)
 

            #########################################
            # Prepare BK 4053
            #########################################
           
            # update the pulse of the BK 4053
            prepare_bk4053(self)

            #########################################
            # Init DDS
            #########################################
 
            init_dds(self, attenuation = self.dds_attenuation * dB, amplitude_dBm = self.dds_amplitude_dBm)

            #########################################
            # DDS programming of ramp
            #########################################
           
            # high frequency
            Omega_b_start = FREQ_AOM + (1/WAVELENGTH * self.slowing_vel_high + self.current_velocity_frequency_shift)/1.0e6

            # low frequency            
            Omega_a_stop  = FREQ_AOM + (1/WAVELENGTH * self.slowing_vel_low + self.current_velocity_frequency_shift)/1.0e6
            print(f"slowing start in frequency {Omega_b_start}")
            print(f"slowing stop in frequency {Omega_a_stop}")

            if Omega_b_start > DDS_MAX:
                print('Error. Omega_b too high. {0:.1f}/{1:.1f}'.format(Omega_b_start, Omega_a_stop))
                Omega_b_start = 10.0
            if Omega_a_stop < 10.0:
                print('Error. Omega_a too low. {0:.1f}/{1:.1f}'.format(Omega_b_start, Omega_a_stop))
                Omega_a_stop = 10.0

                
            # calculate ramp
            (frequency_interval, frequency_interval_ram, ramp_step_size) = prepare_dds_ramp(self,
                    start    = Omega_b_start, # start freq in MHz
                    stop     = Omega_a_stop, # stop freq in MHz
                    duration = self.slowing_laser_duration * ms, # duration of ramp
                    min_no   = 1e3 # number of points on the ramp
                    #min_no   = 5 # number of points on the ramp
            )

            # program the RAM of the DDS
            prg_freq_ramp(self, 
                    profile                 = 0,
                    mode                    = ad9910.RAM_MODE_RAMPUP,
                    frequency_interval      = frequency_interval,
                    frequency_interval_ram  = frequency_interval_ram,
                    step_size               = ramp_step_size
                    )


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
                    
                    # Dictionary to display averaged data
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
            
    return


###################################################################################

def my_run(self):

    # check if scan parameter range and scan function is ok
    if self.scan_ok:
        
        counter = 0
    
        ###########################################################
        # Loop over set points
        ###########################################################    

        for my_ind in range(len(self.scan_values)):
    
            self.scan_index = my_ind

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

                    # Dictionary to display averaged data
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
            
        dds_off(self)

    return


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
    
            self.scan_index = 0
            
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



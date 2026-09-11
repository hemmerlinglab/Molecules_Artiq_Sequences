from artiq.experiment import *

import artiq.coredevice.sampler as splr
import numpy as np
import os

from my_instrument_functions import get_wavemeter_readings


#######################################################################################################

def readout_data(self):
    
    ############################################################################################
    # readout ADC data from Artiq by toggling through all channels and saving the data in a list
    ############################################################################################
    
    self.smp_data = {}
    for channel in self.smp_data_sets.keys():
        # self.smp_data['absorption'] = ...
        self.smp_data[self.smp_data_sets[channel]] = np.array(list(map(lambda v : splr.adc_mu_to_volt(v), self.get_dataset(channel))))


    ###############################
    # Read laser frequencies
    ###############################

    try:
        self.wavemeter_frequencies = get_wavemeter_readings(mode = self.wavemeter_mode)
    except:
        self.wavemeter_frequencies = [0.0, 0.0]

    # save initial Moglabs frequency at first shot
    if self.scan_index == 0:
        
        self.wavemeter_moglabs_frequency = 282.891282
        
        #self.wavemeter_moglabs_frequency = self.wavemeter_frequencies[1]
        #print(self.wavemeter_frequencies)

    ###############################
    # Read repetition rate of comb
    ###############################

    try:
        self.comb_frep = self.frequency_comb.get_frep()
    except:
        self.comb_frep = 0.0

    
    ###############################
    # read spectrum of beat node
    ###############################

    try:
        self.beat_node_fft = self.spectrum_analyzer.get_trace()
    except:
        self.beat_node_fft = np.transpose(np.vstack([ [0] * 801, [0] * 801 ] ))


    #################################################
    # read scope traces of the transfer lock cavity
    #################################################

    if 'scope_transfer_cavity' in self.which_instruments:

        try:
            hlp = self.scope_transfer_cavity.read_all_channels()

            self.transfer_lock_traces = hlp[1:, :]
            self.transfer_lock_times  = hlp[0, :]
        except:
            self.transfer_lock_traces = np.array( 4 * [999 * [0]] )
            self.transfer_lock_times  = np.zeros(999)
    else:
        self.transfer_lock_traces = np.array( 4 * [999 * [0]] )
        self.transfer_lock_times  = np.zeros(999)


    return


#######################################################################################################

def check_shot(self):

    # Function checks if Yag was present and other thigns

    repeat_shot = False

    # check if Yag has fired
    if self.yag_check and np.max(self.smp_data['fire_check']) < 0.1:
        repeat_shot = True
        print('No Yag val: {0}'.format(np.max(self.smp_data['fire_check'])))
        os.system('mpg321 -quiet ~/klaxon.mp3')

    # check if spectroscopy light was there    
    
    blue_min = 0.15/ 1200.0 * 400
    if self.blue_check:
        if np.mean(self.smp_data['int_chamber_pickup']) < blue_min:
           repeat_shot = True

        if repeat_shot:
            #print('No spectroscopy')
            print('No spectroscopy val: {0}'.format(np.max(self.smp_data['int_chamber_pickup'])))
            os.system('mpg321 -quiet ~/klaxon.mp3')

    # check if laser is locked by comparing wavemeter frequency with setpoint

    if self.wavemeter_lock_check:

        # check if comb is still in lock

        if (self.wavemeter_frequencies[1] - self.wavemeter_moglabs_frequency) * 1e12/1e6 > 20.0:

            repeat_shot = True

            print('Moglabs laser offlock')
            os.system('mpg321 -quiet ~/klaxon.mp3')

    return repeat_shot


#######################################################################################################

def integrate_time_trace(self, tag, channel = 0, tstart = 0.0, tstop = 0.0):

    ind1 = int(tstart * 1e3/self.time_step_size)
    ind2 = int(tstop  * 1e3/self.time_step_size)

    self.smp_data_avg[tag] = np.mean(self.channels_avg[self.current_configuration][channel][ind1:ind2])

    return


#######################################################################################################

def average_data(self, i_avg):

    ###############################################################################
    # the average_data function is for display purposes only
    ###############################################################################

    ####################################################
    # offset subtraction and averaging of time traces
    ####################################################

    offset_points = 20

    for k in range(8):
        
        hlp_ds = self.smp_data[self.smp_data_sets['ch' + str(k)]]
        
        # offset subtract if in-cell or PMTs
        if k in [0, 2, 6]:
            hlp_ds = hlp_ds - np.mean(hlp_ds[0:offset_points])

        # average data sets
        self.channels_avg[self.current_configuration][k] = ( self.channels_avg[self.current_configuration][k] * i_avg + hlp_ds ) / (i_avg + 1.0)

    ##########################################
    # Integrate signals for display purposes
    ##########################################
    
    integrate_time_trace(self, 'absorption', channel = 0, tstart = self.slice_min, tstop = self.slice_max)
    integrate_time_trace(self, 'fire_check', channel = 1, tstart = 5.0, tstop = 7.0)
    integrate_time_trace(self, 'pmt',        channel = 2, tstart = self.pmt_slice_min, tstop = self.pmt_slice_max)
    integrate_time_trace(self, 'sat_spec',   channel = 7, tstart = 0.0, tstop = 30.0)

    return


###################################################################################

def update_data_sets(self, counter, n):
   
    # <Counter> toggles through each shot, including averages
    # <n> toggles through the number of set points

    ###########################################################
    # Update sampler data
    ###########################################################
    
    # toggle through channels
    for k in range(8):
        
        # For display purposes only
        
        #self.set_dataset('ch{0}_cfg{1}_avg'.format(k, self.current_configuration), self.channels_avg[self.current_configuration][k], broadcast = True)

        hlp_data = self.channels_avg[self.current_configuration][k]

        self.mutate_dataset('ch{0}_cfg{1}_avg'.format(k, self.current_configuration), n, hlp_data)


        # save each successful shot in ch<number>_cfg{1}_arr datasets
        
        hlp_data = self.smp_data[self.smp_data_sets['ch' + str(k)]]

        self.mutate_dataset('ch{0}_cfg{1}_arr'.format(k, self.current_configuration), (counter), hlp_data)


    ###########################################################
    # Save scan parameters for configuration 0 only
    # since they are the same for all configurations
    ###########################################################
    
    if (self.current_configuration == 0) or (len(self.configurations) == 1):
        
        # update remaining datasets

        self.mutate_dataset('set_points',          counter, self.current_setpoint)
        self.mutate_dataset('act_freqs',           counter, self.wavemeter_frequencies)
  
        self.mutate_dataset('beat_node_fft',       counter, self.beat_node_fft)
        self.mutate_dataset('frequency_comb_frep', counter, self.comb_frep)
        self.mutate_dataset('EOM_frequency',       counter, self.EOM_frequency)
        
        self.mutate_dataset('transfer_lock_traces', counter, self.transfer_lock_traces)
        self.mutate_dataset('transfer_lock_times',  counter, self.transfer_lock_times)

        # spectra = sums over time traces

        self.mutate_dataset('in_cell_spectrum',    n,       self.smp_data_avg['absorption'])
        self.mutate_dataset('pmt_spectrum',        n,       self.smp_data_avg['pmt'])    
        self.mutate_dataset('sat_spectrum',        n,       self.smp_data_avg['sat_spec'])    
        self.mutate_dataset('yag_spectrum',        n,       self.smp_data_avg['fire_check'])    


    return


###################################################################################

def update_data_sets_raster(self, counter, nx, ny):
   
    # Counter toggles through each shot including averages
    # n toggles through the set points

    ###########################################################
    # Display average signals
    # For display purposes only
    ###########################################################
    
    for k in range(8):
        self.set_dataset('ch{0}_cfg{1}_avg'.format(k, self.current_configuration), self.channels_avg[self.current_configuration][k], broadcast = True)

    ###########################################################
    # Save scan parameters for configuration 0 only
    # since they are the same for all configurations
    ###########################################################
    
    if (self.current_configuration == 0) or (len(self.configurations) == 1):
        # this updates the gui for every shot
        self.mutate_dataset('set_points',       counter, self.current_setpoint)
        self.mutate_dataset('act_freqs',        counter, self.wavemeter_frequencies)

        #self.mutate_dataset('in_cell_spectrum', n,       self.smp_data_avg['absorption'])
        #self.mutate_dataset('pmt_spectrum',     n,       self.smp_data_avg['pmt'])    
  
        self.mutate_dataset('beat_node_fft',        counter,  self.beat_node_fft)
        self.mutate_dataset('frequency_comb_frep',  counter,  self.comb_frep)
        self.mutate_dataset('EOM_frequency',        counter,  self.EOM_frequency)
        
    ###########################################################
    # Save raster image
    ###########################################################

    slice_ind = ((nx,nx+1), (ny,ny+1))
    self.mutate_dataset('target_img_incell', slice_ind, self.smp_data_avg['absorption'])

    ###########################################################
    # Save time traces in correct configuration data array
    ###########################################################
    
    # save each successful shot in ch<number>_cfg{1}_arr datasets

    # toggle through channels
    for k in range(8):

        slice_ind = (counter)
        hlp_data = self.smp_data[self.smp_data_sets['ch' + str(k)]]

        self.mutate_dataset('ch{0}_cfg{1}_arr'.format(k, self.current_configuration), slice_ind, hlp_data)

    return




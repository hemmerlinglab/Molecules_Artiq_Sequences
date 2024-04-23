from artiq.experiment import *
#import artiq.coredevice.sampler as splr
import numpy as np
import os

import sys
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")

from helper_functions import *
from scan_functions import scan_parameter

sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server")
from rigol import Rigol_RSA3030, Rigol_DSG821
from frequency_comb import DFC
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server/Windfreak")
from microwave_windfreak import Microwave






#######################################################################################################

def readout_data(self):
    
    # readout data from Artiq by toggling through all channels and saving the data in a list
    self.smp_data = {}
    for channel in self.smp_data_sets.keys():
        # self.smp_data['absorption'] = ...
        self.smp_data[self.smp_data_sets[channel]] = np.array(list(map(lambda v : splr.adc_mu_to_volt(v), self.get_dataset(channel))))

    # read laser frequencies
    self.wavemeter_frequencies = get_wavemeter_readings()

    # read repetition rate of comb
    try:
        self.comb_frep = self.frequency_comb.get_frep()
    except:
        self.comb_frep = 0.0

    # read spectrum of beat node
    try:
        self.beat_node_fft = self.spectrum_analyzer.get_trace()
    except:
        self.beat_node_fft = np.transpose(np.vstack([ [0] * 801, [0] * 801 ] ))

    return


def readout_data_no_freq(self):
    
    # readout data from Artiq by toggling through all channels and saving the data in a list
    self.smp_data = {}
    for channel in self.smp_data_sets.keys():
        # self.smp_data['absorption'] = ...
        self.smp_data[self.smp_data_sets[channel]] = np.array(list(map(lambda v : splr.adc_mu_to_volt(v), self.get_dataset(channel))))

    return




###################################################################################

#def sub_average_data(self, ds, channel, i_avg):
#
#    # integrate the time trace between slice_min and slice_max and average
#    if i_avg == 0:
#        # first average
#        self.smp_data_avg[self.smp_data_sets[channel]]  = ds
#    else:
#        self.smp_data_avg[self.smp_data_sets[channel]] += ds * (i_avg)/(i_avg+1.0)
#
#    return


def average_data(self, i_avg):

    ###############################################################################
    # the following are for display purposes only
    # it continuously updates the averaged data
    ###############################################################################

    # offset subtraction for absorption
    offset_points = 20

    hlp1 = self.smp_data[self.smp_data_sets['ch0']]
    hlp2 = self.smp_data[self.smp_data_sets['ch5']]

    ## subtract the offset

    # subtract offset from the endpoints
    #hlp1 = hlp1 - np.mean(hlp1[:-offset_points])
    #hlp2 = hlp2 - np.mean(hlp2[:-offset_points])

    # subtract offset from the beginning
    hlp1 = hlp1 - np.mean(hlp1[0:offset_points])
    hlp2 = hlp2 - np.mean(hlp2[0:offset_points])


    if i_avg == 0:
        
        # calculate the absorption - absorption reference
        self.ch0_avg = hlp1 - hlp2

        self.ch1_avg = self.smp_data[self.smp_data_sets['ch1']]
        self.ch2_avg = self.smp_data[self.smp_data_sets['ch2']]
        self.ch3_avg = self.smp_data[self.smp_data_sets['ch3']]
        self.ch4_avg = self.smp_data[self.smp_data_sets['ch4']]
        self.ch5_avg = self.smp_data[self.smp_data_sets['ch5']]
        self.ch6_avg = self.smp_data[self.smp_data_sets['ch6']]
        self.ch7_avg = self.smp_data[self.smp_data_sets['ch7']]
        
        #self.ch5_avg = self.ch0_avg
        
    else:
        self.ch0_avg = (self.ch0_avg * (i_avg) + (hlp1 - hlp2) ) / (i_avg+1.0)

        self.ch1_avg = (self.ch1_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch1']]) / (i_avg+1.0)
        self.ch2_avg = (self.ch2_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch2']]) / (i_avg+1.0)
        self.ch3_avg = (self.ch3_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch3']]) / (i_avg+1.0)
        self.ch4_avg = (self.ch4_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch4']]) / (i_avg+1.0)
        self.ch5_avg = (self.ch5_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch5']]) / (i_avg+1.0)
        self.ch6_avg = (self.ch6_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch6']]) / (i_avg+1.0)
        self.ch7_avg = (self.ch7_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch7']]) / (i_avg+1.0)

        #self.ch5_avg = self.ch0_avg


   
    ## toggle through all channels and average the data
    ## ch0, ch1, ch2, ...
    #for channel in self.smp_data_sets.keys():

    #    # get each data set
    #    # self.smp_data['pmt_spectrum'] = ...
    #    ds = self.smp_data[self.smp_data_sets[channel]]

    #    self.sub_average_data(ds[ind_1:ind_2], channel, i_avg)

    # toggle through all channels and average the data


    # integrate pmt signal
    # get time slices for each channel
    pmt_ind_1 = int(self.pmt_slice_min * 1e3/self.time_step_size)
    pmt_ind_2 = int(self.pmt_slice_max * 1e3/self.time_step_size)

    channel = 'pmt'
    self.smp_data_avg[channel] = np.mean(self.ch2_avg[pmt_ind_1:pmt_ind_2])

    # integrate in-cell signal
    # get time slices for each channel
    ind_1 = int(self.slice_min * 1e3/self.time_step_size)
    ind_2 = int(self.slice_max * 1e3/self.time_step_size)

    channel = 'absorption'
    self.smp_data_avg[channel] = np.mean(self.ch0_avg[ind_1:ind_2])


    return

def average_data_calibration(self, i_avg):

    ###############################################################################
    # the following are for display purposes only
    # it continuously updates the averaged data
    ###############################################################################

    # offset subtraction for absorption
    offset_points = 20

    hlp1 = self.smp_data[self.smp_data_sets['ch1']]
    hlp2 = self.smp_data[self.smp_data_sets['ch2']]

    ## subtract the offset
    ## subtract offset from the beginning
    #hlp1 = hlp1 - np.mean(hlp1[0:offset_points])
    #hlp2 = hlp2 - np.mean(hlp2[0:offset_points])

    if i_avg == 0:
        
        # calculate the absorption - absorption reference
        self.ch0_avg = hlp1 - hlp2

        self.ch1_avg = self.smp_data[self.smp_data_sets['ch1']]
        self.ch2_avg = self.smp_data[self.smp_data_sets['ch2']]
        #self.ch3_avg = self.smp_data[self.smp_data_sets['ch3']]
        #self.ch4_avg = self.smp_data[self.smp_data_sets['ch4']]
        
        #self.ch5_avg = self.ch0_avg
        
    else:
        self.ch0_avg = (self.ch0_avg * (i_avg) + (hlp1 - hlp2) ) / (i_avg+1.0)

        self.ch1_avg = (self.ch1_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch1']]) / (i_avg+1.0)
        self.ch2_avg = (self.ch2_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch2']]) / (i_avg+1.0)
        #self.ch3_avg = (self.ch3_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch3']]) / (i_avg+1.0)
        #self.ch4_avg = (self.ch4_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch4']]) / (i_avg+1.0)

        #self.ch5_avg = self.ch0_avg


    # get time slices for each channel
    ind_1 = int(self.slice_min * 1e3/self.time_step_size)
    ind_2 = int(self.slice_max * 1e3/self.time_step_size)

    # for Rb absorption
    channel = 'absorption_spec'
    self.smp_data_avg[channel] = np.mean(self.ch0_avg[ind_1:ind_2])


    return


###################################################################################

def update_data(self, counter, n, slowing_data = False):
   
    # counter is the current shot number
    # n is the current setpoint number

    if not slowing_data:
        # this updates the gui for every shot
        self.mutate_dataset('set_points',       counter, self.current_setpoint)
        self.mutate_dataset('act_freqs',        counter, self.wavemeter_frequencies)

        self.mutate_dataset('in_cell_spectrum', n,       self.smp_data_avg['absorption'])
        self.mutate_dataset('pmt_spectrum',     n,       self.smp_data_avg['pmt'])    
  
        self.mutate_dataset('beat_node_fft',        counter,  self.beat_node_fft)
        self.mutate_dataset('frequency_comb_frep',  counter,  self.comb_frep)
        self.mutate_dataset('EOM_frequency',        counter,  self.EOM_frequency)

    # display average signals
    self.set_dataset('ch0_avg', self.ch0_avg, broadcast = True)
    self.set_dataset('ch1_avg', self.ch1_avg, broadcast = True)
    self.set_dataset('ch2_avg', self.ch2_avg, broadcast = True)
    self.set_dataset('ch3_avg', self.ch3_avg, broadcast = True)
    self.set_dataset('ch4_avg', self.ch4_avg, broadcast = True)
    self.set_dataset('ch5_avg', self.ch5_avg, broadcast = True)
    self.set_dataset('ch6_avg', self.ch6_avg, broadcast = True)
    self.set_dataset('ch7_avg', self.ch7_avg, broadcast = True)

    # save each successful shot in ch<number>_arr datasets
    # needs fixing since the number of channels is hardcoded here
    for k in range(8):
        slice_ind = (counter)
        hlp_data = self.smp_data[self.smp_data_sets['ch' + str(k)]]

        if slowing_data:
            self.mutate_dataset('ch' + str(k) + '_slow_arr', slice_ind, hlp_data)
        else:
            self.mutate_dataset('ch' + str(k) + '_arr', slice_ind, hlp_data)

    ## save data after some averaged shots to avoid data loss
    #if (counter % (3*self.no_of_averages) == 0): 
    #    # and (counter % self.no_of_averages == 0)
    #    print(self.no_of_averages) 
    #    print('Temp saving data ... counter = {0}'.format(counter))

    #    # save data
    #    save_all_data(self)

    #    # save config
    #    save_config(self.basefilename, self.config_dict)

    return


def update_data_no_freq(self, counter, n, slowing_data = False):
   
    # counter is the current shot number
    # n is the current setpoint number

    if not slowing_data:
        # this updates the gui for every shot
        self.mutate_dataset('set_points',       counter, self.current_setpoint)

        self.mutate_dataset('in_cell_spectrum', n,       self.smp_data_avg['absorption'])
        self.mutate_dataset('pmt_spectrum',     n,       self.smp_data_avg['pmt'])    
  
        self.mutate_dataset('EOM_frequency',        counter,  self.EOM_frequency)

    # display average signals
    self.set_dataset('ch0_avg', self.ch0_avg, broadcast = True)
    self.set_dataset('ch1_avg', self.ch1_avg, broadcast = True)
    self.set_dataset('ch2_avg', self.ch2_avg, broadcast = True)
    self.set_dataset('ch3_avg', self.ch3_avg, broadcast = True)
    self.set_dataset('ch4_avg', self.ch4_avg, broadcast = True)
    self.set_dataset('ch5_avg', self.ch5_avg, broadcast = True)
    self.set_dataset('ch6_avg', self.ch6_avg, broadcast = True)
    self.set_dataset('ch7_avg', self.ch7_avg, broadcast = True)

    # save each successful shot in ch<number>_arr datasets
    # needs fixing since the number of channels is hardcoded here
    for k in range(8):
        slice_ind = (counter)
        hlp_data = self.smp_data[self.smp_data_sets['ch' + str(k)]]

        if slowing_data:
            self.mutate_dataset('ch' + str(k) + '_slow_arr', slice_ind, hlp_data)
        else:
            self.mutate_dataset('ch' + str(k) + '_arr', slice_ind, hlp_data)

    ## save data after some averaged shots to avoid data loss
    #if (counter % (3*self.no_of_averages) == 0): 
    #    # and (counter % self.no_of_averages == 0)
    #    print(self.no_of_averages) 
    #    print('Temp saving data ... counter = {0}'.format(counter))

    #    # save data
    #    save_all_data(self)

    #    # save config
    #    save_config(self.basefilename, self.config_dict)

    return

     
def update_data_raster(self, counter, nx, ny):
    # this updates the gui for every shot
    
    #print(self.get_dataset('target_img_incell'))
    slice_ind = ((nx,nx+1), (ny,ny+1))
    self.mutate_dataset('target_img_incell', slice_ind, self.smp_data_avg['absorption'])

    # save each successful shot in ch<number>_arr datasets
    # needs fixing since the number of channels is hardcoded here
    for k in range(5):
        slice_ind = (counter)
        hlp_data = self.smp_data[self.smp_data_sets['ch' + str(k)]]

        self.mutate_dataset('ch' + str(k) + '_arr', slice_ind, hlp_data)

    # display average signals
    self.set_dataset('ch0_avg', self.ch0_avg, broadcast = True)
    self.set_dataset('ch1_avg', self.ch1_avg, broadcast = True)
    self.set_dataset('ch2_avg', self.ch2_avg, broadcast = True)
    self.set_dataset('ch3_avg', self.ch3_avg, broadcast = True)
    self.set_dataset('ch4_avg', self.ch4_avg, broadcast = True)
    self.set_dataset('ch5_avg', self.ch5_avg, broadcast = True)
    self.set_dataset('ch6_avg', self.ch6_avg, broadcast = True)
    self.set_dataset('ch7_avg', self.ch7_avg, broadcast = True)


    return




def update_data_calibration(self, counter, n, last_point = True, slowing_data = False):
    # this updates the gui for every shot
    self.mutate_dataset('set_points', counter, self.current_setpoint)
    self.mutate_dataset('act_freqs', counter, self.wavemeter_frequencies)
    
    ## average over time trace to display
    if last_point:
        # only plot once all averages are taken
        self.mutate_dataset('rb_spectrum',     n, self.smp_data_avg['absorption_spec'])

    # display average signals
    self.set_dataset('ch0_avg', self.ch0_avg, broadcast = True)
    self.set_dataset('ch1_avg', self.ch1_avg, broadcast = True)
    self.set_dataset('ch2_avg', self.ch2_avg, broadcast = True)
    self.set_dataset('ch3_avg', self.ch0_avg, broadcast = True)
    self.set_dataset('ch4_avg', self.ch0_avg, broadcast = True)
    self.set_dataset('ch5_avg', self.ch0_avg, broadcast = True)
    self.set_dataset('ch6_avg', self.ch0_avg, broadcast = True)
    self.set_dataset('ch7_avg', self.ch0_avg, broadcast = True)

    # save each successful shot in ch<number>_arr datasets
    # needs fixing since the number of channels is hardcoded here
    for k in range(8):
        slice_ind = (counter)
        hlp_data = self.smp_data[self.smp_data_sets['ch' + str(k)]]

        if slowing_data:
            self.mutate_dataset('ch' + str(k) + '_slow_arr', slice_ind, hlp_data)
        else:
            self.mutate_dataset('ch' + str(k) + '_arr', slice_ind, hlp_data)

    return


def check_shot(self):
    repeat_shot = False

    # check if Yag has fired
    if self.yag_check and np.max(self.smp_data['fire_check']) < 0.025:
        repeat_shot = True
        print('No Yag')
        os.system('mpg321 -quiet ~/klaxon.mp3')

    # check if spectroscopy light was there
    blue_min = splr.adc_mu_to_volt(15)
    if self.blue_check:
        if self.which_scanning_laser == 1:
          if np.min(self.smp_data['davos_pickup']) < blue_min:
                repeat_shot = True

        elif self.which_scanning_laser == 2:
          if np.min(self.smp_data['hodor_pickup']) < blue_min:
                repeat_shot = True

        elif self.which_scanning_laser == 3:
          if np.min(self.smp_data['daenerys_pickup']) < blue_min:
                repeat_shot = True
        else:
            print('Not checking spectroscopy laser')

        if repeat_shot:
            print('No spectroscopy')
            os.system('mpg321 -quiet ~/klaxon.mp3')

    return repeat_shot



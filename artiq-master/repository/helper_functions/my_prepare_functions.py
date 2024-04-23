from artiq.experiment import *

import os
import datetime
import shutil
import numpy as np
from configparser import ConfigParser

from scan_functions          import scan_parameter
from my_instrument_functions import prepare_initial_instruments
from base_sequences          import reset_core


#######################################################################################################

def my_prepare(self, data_to_save = None):

    # prepare datasets
    prepare_datasets(self)
    
    # sets all instruments and parameters before the scan
    prepare_initial_instruments(self)
    
    # prepare config file
    prepare_saving_configuration(self, data_to_save = data_to_save)

    reset_core(self)

    return


#######################################################################################################

def prepare_datasets(self):

    # Scan interval
    self.scan_values = np.linspace(self.min_scan_value, self.max_scan_value, self.setpoint_count)

    # Check scan range
    self.scan_ok = scan_parameter(self, 0, scan_check = True)

    # Prepare some data sets
    self.smp_data_sets = {
            'ch0' : 'absorption',   # in-cell
            'ch1' : 'fire_check',   # yag photodiode check
            'ch2' : 'pmt',          # pmt
            'ch3' : 'hodor_pickup', # Hodor blue pickup
            'ch4' : 'davos_pickup', # Davos blue pickup
            'ch5' : 'yag_sync',     # Yag sync
            'ch6' : 'daenerys_pickup', # Daenerys pickup
            'ch7' : 'in_cell_ref'      # in-cell ref
            }

    self.time_interval = np.linspace(0,(self.time_step_size+9)*(self.scope_count-1)/1.0e3,self.scope_count)

    self.set_dataset('set_points', ([0] * (self.no_of_averages * self.setpoint_count)),broadcast=True)
    self.set_dataset('act_freqs',  ([0] * (self.no_of_averages * self.setpoint_count)),broadcast=True)
    self.set_dataset('freqs',      (self.scan_values),broadcast=True)
    self.set_dataset('times',      (self.time_interval),broadcast=True)

    # data set without slowing
    self.set_dataset('ch0_arr',       ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch1_arr',       ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch2_arr',       ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch3_arr',       ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch4_arr',       ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch5_arr',       ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch6_arr',       ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch7_arr',       ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)

    # data set with slowing
    self.set_dataset('ch0_slow_arr',  ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch1_slow_arr',  ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch2_slow_arr',  ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch3_slow_arr',  ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch4_slow_arr',  ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch5_slow_arr',  ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch6_slow_arr',  ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)
    self.set_dataset('ch7_slow_arr',  ([[0] * len(self.time_interval)] * self.no_of_averages * self.setpoint_count),broadcast=True)

    # dataset only for plotting average signals
    self.set_dataset('ch0_avg',  ([0] * len(self.time_interval)),broadcast=True)
    self.set_dataset('ch1_avg',  ([0] * len(self.time_interval)),broadcast=True)
    self.set_dataset('ch2_avg',  ([0] * len(self.time_interval)),broadcast=True)
    self.set_dataset('ch3_avg',  ([0] * len(self.time_interval)),broadcast=True)
    self.set_dataset('ch4_avg',  ([0] * len(self.time_interval)),broadcast=True)
    self.set_dataset('ch5_avg',  ([0] * len(self.time_interval)),broadcast=True)
    self.set_dataset('ch6_avg',  ([0] * len(self.time_interval)),broadcast=True)
    self.set_dataset('ch7_avg',  ([0] * len(self.time_interval)),broadcast=True)

    if self.scanning_laser == 'Hodor':
        self.which_scanning_laser = 2
    elif self.scanning_laser == 'Davos':
        self.which_scanning_laser = 1
    elif self.scanning_laser == 'Daenerys':
        self.which_scanning_laser = 3

    # parameters for comb
    self.set_dataset('frequency_comb_frep',  ([0] * self.no_of_averages * self.setpoint_count), broadcast=True)
    self.set_dataset('EOM_frequency',  ([0] * self.no_of_averages * self.setpoint_count), broadcast=True)
    self.set_dataset('beat_node_fft',  ([np.zeros([801, 2])] * self.no_of_averages * self.setpoint_count), broadcast=True)


    # spectrum datasets    
    self.set_dataset('in_cell_spectrum',     ([0] * self.setpoint_count),broadcast=True)
    self.set_dataset('pmt_spectrum',         ([0] * self.setpoint_count),broadcast=True)


    return


#######################################################################################################

def prepare_saving_configuration(self, data_to_save = None):

    # Saving data configurations

    if data_to_save == None:
        self.data_to_save = [
                         {'var' : 'set_points', 'name' : 'set_points'},
                         {'var' : 'act_freqs', 'name' : 'actual frequencies (wavemeter)'},
                         {'var' : 'freqs', 'name' : 'freqs'},
                         {'var' : 'times', 'name' : 'times'},
                         {'var' : 'ch0_arr', 'name' : self.smp_data_sets['ch0']},
                         {'var' : 'ch1_arr', 'name' : self.smp_data_sets['ch1']},
                         {'var' : 'ch2_arr', 'name' : self.smp_data_sets['ch2']},
                         {'var' : 'ch3_arr', 'name' : self.smp_data_sets['ch3']},
                         {'var' : 'ch4_arr', 'name' : self.smp_data_sets['ch4']},
                         {'var' : 'ch5_arr', 'name' : self.smp_data_sets['ch5']},
                         {'var' : 'ch6_arr', 'name' : self.smp_data_sets['ch6']},
                         {'var' : 'ch7_arr', 'name' : self.smp_data_sets['ch7']},
                         {'var' : 'ch0_slow_arr', 'name' : self.smp_data_sets['ch0']},
                         {'var' : 'ch1_slow_arr', 'name' : self.smp_data_sets['ch1']},
                         {'var' : 'ch2_slow_arr', 'name' : self.smp_data_sets['ch2']},
                         {'var' : 'ch3_slow_arr', 'name' : self.smp_data_sets['ch3']},
                         {'var' : 'ch4_slow_arr', 'name' : self.smp_data_sets['ch4']},
                         {'var' : 'ch5_slow_arr', 'name' : self.smp_data_sets['ch5']},
                         {'var' : 'ch6_slow_arr', 'name' : self.smp_data_sets['ch6']},
                         {'var' : 'ch7_slow_arr', 'name' : self.smp_data_sets['ch7']},
                         {'var' : 'frequency_comb_frep', 'name' : 'Repetition frequency of comb'},
                         {'var' : 'EOM_frequency', 'name' : 'EOM_frequency'},
                         {'var' : 'beat_node_fft', 'name' : 'FFT of beat node with comb'},
                         ]
    else:
        self.data_to_save = data_to_save

    # save sequence file name
    self.config_dict.append({'par' : 'sequence_file', 'val' : self.sequence_filename, 'cmt' : 'Filename of the main sequence file'})

    for k in range(5):
        print("")
    print("*"*100)
    print("* Starting new scan")
    print("*"*100)
    print("")
    print("")

    # get the filename for the scan, e.g. 20190618_105557
    get_basefilename(self)
    
    # save the config
    save_config(self.basefilename, self.config_dict)

    return


#######################################################################################################

def get_basefilename(self, extension = ''):

    my_timestamp = datetime.datetime.today()
    
    self.today = datetime.datetime.today()
    self.today = self.today.strftime('%Y%m%d')

    self.datafolder = '/home/molecules/software/data/'
    #self.setpoint_filename_laser1 = '/home/molecules/skynet/Logs/setpoint.txt'
    #self.setpoint_filename_laser2 = '/home/molecules/skynet/Logs/setpoint2.txt'
 
    basefolder = str(self.today) # 20190618
    # create new folder if doesn't exist yet
    if not os.path.exists(self.datafolder + basefolder):
        os.makedirs(self.datafolder + basefolder)

    self.scan_timestamp = str(my_timestamp.strftime('%Y%m%d_%H%M%S'))

    self.basefilename = self.datafolder + basefolder + '/' + self.scan_timestamp # 20190618_105557

    # add optional extension
    if not extension == '':
        self.basefilename += '_' + str(extension)

        self.scan_timestamp += '_' + str(extension)


#######################################################################################################

def save_config(basefilename, var_dict):

        # save run configuration
        # creates and overwrites config file
        # var_dict is an array of dictionaries
        # var_dict[0] = {
        #    'par': <parameter name>,
        #    'val': <parameter value>,
        #    'unit': <parameter unit>, (optional)
        #    'cmt': <parameter comment> (optional)
        #    }

        optional_parameters = ['unit', 'cmt']        
        conf_filename = basefilename + '_conf'

        # use ConfigParser to save config options
        config = ConfigParser()

        # create config file
        conf_file = open(conf_filename, 'w')
        print('Config file written.')

        # add scan name to config file
        config['Scan'] = {'filename' : basefilename}

        # toggle through dictionary and add the config categories
        for d in var_dict:
            config[d['par']] = {'val' : d['val']}

            for opt in optional_parameters:
                if opt in d.keys():
                    config[d['par']].update({opt : d[opt]})

        config.write(conf_file)

        # save also the sequence file 
        #print(config['sequence_file']['val'])
        #print(basefilename + '_sequence')
        shutil.copyfile(config['sequence_file']['val'], basefilename + '_sequence')
        
        conf_file.close()




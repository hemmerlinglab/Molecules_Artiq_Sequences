from artiq.experiment import *
import artiq.coredevice.sampler as splr
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

def my_setattr(self, arg, val, scannable = True):

    # define the attribute
    self.setattr_argument(arg, val)

    # add each attribute to the config dictionary
    if hasattr(val, 'unit'):
        exec("self.config_dict.append({'par' : arg, 'val' : self." + arg + ", 'unit' : '" + str(val.unit) + "', 'scannable' : " + str(scannable) + "})")
    else:
        exec("self.config_dict.append({'par' : arg, 'val' : self." + arg + ", 'scannable' : " + str(scannable) + "})")


#######################################################################################################

def load_instruments(self):
 
    # Load all instruments specified when calling the base_build
    for instr in self.which_instruments:
        if instr == 'EOM':
            self.EOM_function_generator = Rigol_DSG821()

        if instr == 'frequency_comb':
            self.frequency_comb         = DFC()

        if instr == 'microwave':
            self.microwave              = Microwave()

        if instr == 'spectrum_analyzer':
            self.spectrum_analyzer      = Rigol_RSA3030()

    return

#######################################################################################################

def close_instruments(self):
 
    # Disconnect instruments
    # Load all instruments specified when calling the base_build
    for instr in self.which_instruments:
        if instr == 'EOM':
            self.EOM_function_generator.close()

        if instr == 'frequency_comb':
            self.frequency_comb.close()

        if instr == 'microwave':
            self.microwave.close()

        if instr == 'spectrum_analyzer':
            self.spectrum_analyzer.close()

    return


#######################################################################################################

def load_variables(self):
 
    ###########################################################
    # Base parameters all sequences have in common
    ###########################################################

    self.config_dict = []
    self.wavemeter_frequencies = []
    self.EOM_frequency = 0.0 #None
    self.comb_frep     = None
    self.beat_node_fft = None

    return


#######################################################################################################

def load_attributes(self):

    self.setattr_device('core') # Core Artiq Device (required)
    self.setattr_device('ttl3') # trigger in, sync to pulse tube
    self.setattr_device('ttl4') # flash-lamp
    self.setattr_device('ttl6') # q-switch
    self.setattr_device('ttl5') # uv ccd trigger
    self.setattr_device('ttl8') # slowing shutter
    self.setattr_device('ttl9') # experimental start
    self.setattr_device('ttl7') # uniblitz shutter control
    
    self.setattr_device('ttl11') # cavity scan

    self.setattr_device('sampler0') # adc voltage sampler
    self.setattr_device('sampler1') # adc voltage sampler
    self.setattr_device('scheduler') # scheduler used
    
    self.setattr_device('zotino0') # for analog output voltages

    return


#######################################################################################################

def load_parameters(self):

    # number of time steps
    my_setattr(self, 'scope_count',     NumberValue(default=400,unit='reads per shot',scale=1,ndecimals=0,step=1))

    # number of averages
    my_setattr(self, 'no_of_averages',  NumberValue(default=10,unit='averages',scale=1,ndecimals=0,step=1))

    my_setattr(self, 'time_step_size',  NumberValue(default=100,unit='us',scale=1,ndecimals=0,step=1))
    my_setattr(self, 'slice_min',       NumberValue(default=6,unit='ms',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'slice_max',       NumberValue(default=7,unit='ms',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'pmt_slice_min',   NumberValue(default=5.5,unit='ms',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'pmt_slice_max',   NumberValue(default=7,unit='ms',scale=1,ndecimals=1,step=0.1))

    my_setattr(self, 'relock_wait_time',    NumberValue(default=100,unit='ms',scale=1,ndecimals=1,step=1))
    my_setattr(self, 'lock_wait_time',      NumberValue(default=100,unit='ms',scale=1,ndecimals=1,step=1))
    my_setattr(self, 'relock_laser_steps',  NumberValue(default=3000,unit='',scale=1,ndecimals=0,step=1))

    # High voltage
    my_setattr(self, 'plate_voltage',       NumberValue(default=0,unit='V',type='int',scale=1,ndecimals=0,step=1,min=0,max=30.0e3))

    ##############################
    # General Scanning Parameter
    ##############################
    
    # get all parameters
    list_of_parameters = [x['par'] for x in self.config_dict if x['scannable']]

    my_setattr(self, 'min_scan', NumberValue(default=100,unit='',scale=1,ndecimals=3,step=.001))
    my_setattr(self, 'max_scan', NumberValue(default=200,unit='',scale=1,ndecimals=3,step=.001))
    my_setattr(self, 'steps',    NumberValue(default=100,unit='steps to scan',scale=1,ndecimals=0,step=1))

    # general scanning parameter 
    my_setattr(self, 'scanning_parameter', EnumerationValue(list_of_parameters, default = list_of_parameters[0]))    

    return


#######################################################################################################

def rb_calibration_build(self):
    # EnvExperiment attribute: number of voltage samples per scan
    my_setattr(self, 'scanning_laser',EnumerationValue(['Davos', 'Hodor'],default='Hodor'))
    
    my_setattr(self, 'offset_laser_Hodor',NumberValue(default=377.10701,unit='THz',scale=1,ndecimals=6,step=.000001))

    my_setattr(self, 'repetition_time',NumberValue(default=0.5,unit='s',scale=1,ndecimals=1,step=0.1))
    
    return


#######################################################################################################

def pulsed_scan_build(self):
    # EnvExperiment attribute: number of voltage samples per scan

    my_setattr(self, 'setpoint_count',NumberValue(default=30,unit='setpoints',scale=1,ndecimals=0,step=1))
    my_setattr(self, 'setpoint_min',NumberValue(default=-150,unit='MHz',scale=1,ndecimals=3,step=1))
    my_setattr(self, 'setpoint_max',NumberValue(default=150,unit='MHz',scale=1,ndecimals=3,step=1))
    #my_setattrself, ('which_scanning_laser',NumberValue(default=2,unit='',scale=1,ndecimals=0,step=1))
    my_setattr(self, 'scanning_laser',EnumerationValue(['Davos', 'Hodor', 'Daenerys'],default='Daenerys'))

    # offset of laseself, rs
    my_setattr(self, 'offset_laser_Davos',NumberValue(default=375.763150,unit='THz',scale=1,ndecimals=6,step=.000001))
    my_setattr(self, 'offset_laser_Hodor',NumberValue(default=391.016005,unit='THz',scale=1,ndecimals=6,step=.000001))
    my_setattr(self, 'offset_laser_Daenerys',NumberValue(default=286.86,unit='THz',scale=1,ndecimals=6,step=.000001))

    my_setattr(self, 'yag_fire_time',NumberValue(default=30,unit='ms',scale=1,ndecimals=0,step=1))
    my_setattr(self, 'sampler_delay_time',NumberValue(default=25,unit='ms',scale=1,ndecimals=0,step=1))

    # dewar shutter
    my_setattr(self, 'shutter_start_time',NumberValue(default=15,unit='ms',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'shutter_open_time',NumberValue(default=30,unit='ms',scale=1,ndecimals=1,step=0.1))

    # slowing laser self, shutter
    my_setattr(self, 'slowing_shutter_start_time',NumberValue(default=4.5,unit='ms',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'slowing_shutter_duration',NumberValue(default=60,unit='ms',scale=1,ndecimals=1,step=0.1))

    my_setattr(self, 'repetition_time',NumberValue(default=0.5,unit='s',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'yag_power',NumberValue(default=13,unit='',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'he_flow',NumberValue(default=2,unit='sccm',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'he_flow_wait',NumberValue(default=2,unit='s',scale=1,ndecimals=1,step=0.1))
    
    my_setattr(self, 'pulse_tube_sync_wait',NumberValue(default=10,unit='ms',scale=1,ndecimals=1,step=0.1))
    
    # Boomy_leans
    my_setattr(self, 'yag_check',BooleanValue(default=True))
    my_setattr(self, 'blue_check',BooleanValue(default=False))

    # slowing laser self, shutter
    my_setattr(self, 'slowing_laser_shutter_on',BooleanValue(default=False))
    my_setattr(self, 'uniblitz_on',BooleanValue(default=False))
    
    return


#######################################################################################################

def base_build(self, which_instruments = []):

    #################################
    # Load all instruments
    #################################

    self.which_instruments = which_instruments
    load_instruments(self)

    #################################
    # Load all variables
    #################################

    load_variables(self)

    #################################
    # Load all attributes
    #################################

    load_attributes(self)

    #################################
    # Load all parameters
    #################################

    load_parameters(self)

    return


#######################################################################################################

def my_prepare(self, data_to_save = None):

    prepare_datasets(self)
    
    # sets all instruments and parameters before the scan
    prepare_initial_instruments(self)
    
    prepare_saving_configuration(self, data_to_save = data_to_save)

    return


#######################################################################################################

def reset_scan_parameter(self):
    
    # sets the value of the scanned parameter to the one in the parameter listing

    scan_parameter(self, 0, reset_value = True)

    return


#######################################################################################################

def my_analyze(self):

    # reset scan value to setting in parameter

    reset_scan_parameter(self)

    # function is run after the experiment, i.e. after run() is called
    print('Saving data ...')
    save_all_data(self)

    # overwrite config file with complete configuration
    self.config_dict.append({'par' : 'Status', 'val' : True, 'cmt' : 'Run finished.'})
    save_config(self.basefilename, self.config_dict)

    add_scan_to_list(self)

    print('Scan ' + self.basefilename + ' finished.')
    print('Scan finished.')

    close_instruments(self)

    # Play sound that scan is finished
    os.system('mpg321 -quiet ~/boat.mp3')
    
    return


#######################################################################################################

def prepare_datasets(self):

    # Scan interval
    self.scan_values = np.linspace(self.min_scan, self.max_scan, self.steps)

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
    self.set_dataset('freqs',      (self.scan_interval),broadcast=True)
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

    self.reset_core()

    return


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



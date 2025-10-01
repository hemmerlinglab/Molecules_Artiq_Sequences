from artiq.experiment import *

import numpy as np

from my_instrument_functions    import *
from scan_functions             import get_scannable_parameters


#######################################################################################################

def my_build(self, which_instruments = [], raster_scan = False):

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

    load_parameters(self, raster_scan = raster_scan)

    return


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

def load_variables(self):
 
    ###########################################################
    # Base parameters all sequences have in common
    ###########################################################

    self.config_dict            = []
    self.wavemeter_frequencies  = []
    self.EOM_frequency          = 0.0
    self.comb_frep              = None
    self.beat_node_fft          = None

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

def load_parameters(self, raster_scan = False):

    # number of time steps
    my_setattr(self, 'scope_count',     NumberValue(default=400,unit='reads per shot',scale=1,ndecimals=0,step=1))

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

    #my_setattr(self, 'setpoint_count',NumberValue(default=30,unit='setpoints',scale=1,ndecimals=0,step=1))
    #my_setattr(self, 'setpoint_min',NumberValue(default=-150,unit='MHz',scale=1,ndecimals=3,step=1))
    #my_setattr(self, 'setpoint_max',NumberValue(default=150,unit='MHz',scale=1,ndecimals=3,step=1))

    my_setattr(self, 'yag_fire_time',     NumberValue(default=30,unit='ms',scale=1,ndecimals=0,step=1))
    my_setattr(self, 'sampler_delay_time',NumberValue(default=25,unit='ms',scale=1,ndecimals=0,step=1))

    # dewar shutter
    my_setattr(self, 'shutter_start_time',NumberValue(default=15,unit='ms',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'shutter_open_time', NumberValue(default=30,unit='ms',scale=1,ndecimals=1,step=0.1))

    my_setattr(self, 'repetition_time',NumberValue(default=0.5,unit='s',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'yag_power',      NumberValue(default=13,unit='',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'he_flow',        NumberValue(default=0,unit='sccm',scale=1,ndecimals=1,step=0.1))
    my_setattr(self, 'he_flow_wait',   NumberValue(default=2,unit='s',scale=1,ndecimals=1,step=0.1))
    
    my_setattr(self, 'pulse_tube_sync_wait',NumberValue(default=10,unit='ms',scale=1,ndecimals=1,step=0.1))
   
    ####################################################################
    # Booleans
    ####################################################################
    
    my_setattr(self, 'yag_check',           BooleanValue(default=True))
    my_setattr(self, 'blue_check',          BooleanValue(default=True))
    my_setattr(self, 'uniblitz_on',         BooleanValue(default=False))
    my_setattr(self, 'wavemeter_lock_check',BooleanValue(default=False))
    
    
    my_setattr(self, 'randomize_scan',           BooleanValue(default=False))
    
    
    ####################################################################
    # Laser and Microwave Frequencies
    ####################################################################

    # Microwave
    my_setattr(self, 'microwave_frequency', NumberValue(default = 12577,unit='MHz', min=15.0, max = 20.0e3, scale=1,ndecimals=3,step=1))
    my_setattr(self, 'microwave_power',     NumberValue(default =   -50,unit='dB', min=-100.0, max=10.0, scale=1,ndecimals=1,step=1))
    

    my_setattr(self, 'offset_laser_Davos',      NumberValue(default=375.763150,unit='THz',scale=1,ndecimals=6,step=.000001))
    my_setattr(self, 'offset_laser_Hodor',      NumberValue(default=375.763290,unit='THz',scale=1,ndecimals=6,step=.000001))
    my_setattr(self, 'offset_laser_Daenerys',   NumberValue(default=286.86,unit='THz',scale=1,ndecimals=6,step=.000001))


    ##############################
    # General Scanning Parameter
    ##############################
    
    if not raster_scan:
        # get all parameters
        #list_of_parameters = [x['par'] for x in self.config_dict if x['scannable']]
        list_of_parameters = get_scannable_parameters()

        # offset of lasers
        my_setattr(self, 'scanning_laser',          EnumerationValue(['Davos', 'Hodor', 'Daenerys'],default='Hodor'))

        my_setattr(self, 'min_scan_value', NumberValue(default=100,unit='',scale=1,ndecimals=3,step=.001))
        my_setattr(self, 'max_scan_value', NumberValue(default=200,unit='',scale=1,ndecimals=3,step=.001))

        # general scanning parameter 
        my_setattr(self, 'scanning_parameter', EnumerationValue(list_of_parameters, default = list_of_parameters[0]))    

        # number of scan points
        my_setattr(self, 'setpoint_count', NumberValue(default=10,unit='steps to scan',scale=1,ndecimals=0,step=1,min=1))

    else:        

        # offset of lasers
        my_setattr(self, 'scanning_laser',          EnumerationValue(['Davos', 'Hodor', 'Daenerys'],default='Hodor'))

        my_setattr(self, 'min_scan_value', NumberValue(default=1,unit='',scale=1,ndecimals=3,step=.001))
        my_setattr(self, 'max_scan_value', NumberValue(default=2,unit='',scale=1,ndecimals=3,step=.001))

        my_setattr(self, 'scanning_parameter', EnumerationValue(['dummy'], default = 'dummy'))

        # x
        my_setattr(self, 'min_x',NumberValue(default=3.5,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'max_x',NumberValue(default=4.6,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'steps_x',NumberValue(default=3,unit='',scale=1,ndecimals=0,step=1))
        
        # y
        my_setattr(self, 'min_y',NumberValue(default=3.25,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'max_y',NumberValue(default=5.50,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'steps_y',NumberValue(default=3,unit='',scale=1,ndecimals=0,step=1))
        
        my_setattr(self, 'setpoint_count', NumberValue(default=2,unit='steps to scan',scale=1,ndecimals=0,step=1, min = 1))


    # number of averages
    my_setattr(self, 'no_of_averages',  NumberValue(default=3,unit='averages',scale=1,ndecimals=0,step=1))

    return



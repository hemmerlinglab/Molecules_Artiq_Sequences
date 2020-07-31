# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime
import os
import time
import csv

import sys
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")

from helper_functions import *


# every Experiment needs a build and a run function
class Scan_Single_Laser(EnvExperiment):
    def build(self):

        self.config_dict = []
        self.wavemeter_frequencies = []
        
        self.setattr_device('core') # Core Artiq Device (required)
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('ttl5') # uv ccd trigger
        self.setattr_device('ttl8') # slowing shutter
        self.setattr_device('ttl9') # experimental start

        self.setattr_device('sampler0') # adc voltage sampler
        self.setattr_device('scheduler') # scheduler used

        # EnvExperiment attribute: number of voltage samples per scan
        self.my_setattr('scope_count',NumberValue(default=400,unit='reads per shot',scale=1,ndecimals=0,step=1))
        self.my_setattr('scan_count',NumberValue(default=2,unit='averages',scale=1,ndecimals=0,step=1))
        
        self.my_setattr('setpoint_count',NumberValue(default=3,unit='setpoints',scale=1,ndecimals=0,step=1))
        self.my_setattr('setpoint_min',NumberValue(default=-750,unit='MHz',scale=1,ndecimals=0,step=1))
        self.my_setattr('setpoint_max',NumberValue(default=1500,unit='MHz',scale=1,ndecimals=0,step=1))
        self.my_setattr('which_scanning_laser',NumberValue(default=1,unit='',scale=1,ndecimals=0,step=1))
        
        # offset of lasers
        self.my_setattr('offset_laser1',NumberValue(default=382.11035,unit='THz',scale=1,ndecimals=6,step=.000001))
        self.my_setattr('offset_laser2',NumberValue(default=375.763,unit='THz',scale=1,ndecimals=6,step=.000001))

        self.my_setattr('step_size',NumberValue(default=100,unit='us',scale=1,ndecimals=0,step=1))
        self.my_setattr('slice_min',NumberValue(default=5,unit='ms',scale=1,ndecimals=1,step=0.1))
        self.my_setattr('slice_max',NumberValue(default=6,unit='ms',scale=1,ndecimals=1,step=0.1))
        self.my_setattr('pmt_slice_min',NumberValue(default=5,unit='ms',scale=1,ndecimals=1,step=0.1))
        self.my_setattr('pmt_slice_max',NumberValue(default=6,unit='ms',scale=1,ndecimals=1,step=0.1))

        self.my_setattr('repetition_time',NumberValue(default=0.1,unit='s',scale=1,ndecimals=1,step=0.1))
        self.my_setattr('yag_power',NumberValue(default=5,unit='',scale=1,ndecimals=1,step=0.1))
        self.my_setattr('he_flow',NumberValue(default=3,unit='sccm',scale=1,ndecimals=1,step=0.1))
        
        # Boomy_leans
        self.my_setattr('yag_check',BooleanValue(default=True))
        self.my_setattr('blue_check',BooleanValue(default=True))
        
        self.my_setattr('shutter_on',BooleanValue(default=False))
        
    def my_setattr(self, arg, val):
        
        # define the attribute
        self.setattr_argument(arg,val)

        # add each attribute to the config dictionary
        if hasattr(val, 'unit'):
            exec("self.config_dict.append({'par' : arg, 'val' : self." + arg + ", 'unit' : '" + str(val.unit) + "'})")
        else:
            exec("self.config_dict.append({'par' : arg, 'val' : self." + arg + "})")

    ### Script to run on Artiq
    # Basic Schedule:
    # 1) Trigger YAG Flashlamp
    # 2) Wait 150 us
    # 3) Trigger Q Switch
    # 4) In parallel, read off 2 diodes and PMT
    @kernel
    def fire_and_read(self):
        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        self.sampler0.init() # initializes sampler device
        
        ### Set Channel Gain 
        for i in range(8):
            self.sampler0.set_gain_mu(i,0) # (channel,setting) gain is 10^setting
        
        delay(260*us)
        
        ### Data Variable Initialization
        data0 = [0]*self.scope_count # signal data
        data1 = [0]*self.scope_count # fire check data
        data2 = [0]*self.scope_count # uhv data
        data3 = [0]*self.scope_count # post select, checks spec blue
        data4 = [0]*self.scope_count # post select, checks slow blue
        smp = [0]*8 # individual sample

        ### Fire and sample
        with parallel:
            
            with sequential:
                self.ttl9.pulse(10*us) # experimental start

                delay(10*ms) # additional delay since shutter is slow

                delay(150*us)
                self.ttl4.pulse(15*us) # trigger flash lamp
                delay(135*us) # wait optimal time (see Minilite manual)
                self.ttl6.pulse(15*us) # trigger q-switch
                delay(100*us) # wait until some time after green flash
                self.ttl5.pulse(15*us) # trigger uv ccd

            with sequential:
                if self.shutter_on:
                    # shut slowing laser off from the start
                    self.ttl8.on()
                    delay(500*ms)
                    self.ttl8.off()


            with sequential:
                for j in range(self.scope_count):
                    self.sampler0.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
                    data0[j] = smp[0]
                    data1[j] = smp[1]
                    data2[j] = smp[2]
                    data3[j] = smp[3]
                    data4[j] = smp[4]
                    #delay(5*us)
                    delay(self.step_size*us) # plus 9us from sample_mu

        ### Allocate and Transmit Data All Channels
        self.set_dataset('ch0', (data0), broadcast = True)
        self.set_dataset('ch1', (data1), broadcast = True)
        self.set_dataset('ch2', (data2), broadcast = True)
        self.set_dataset('ch3', (data3), broadcast = True)
        self.set_dataset('ch4', (data4), broadcast = True)

    def prepare(self):
        # function is run before the experiment, i.e. before run() is called

        self.smp_data_sets = {
                'ch0' : 'absorption',
                'ch1' : 'fire_check',
                'ch2' : 'pmt',
                'ch3' : 'spec_check',
                'ch4' : 'slow_check'
                }

        self.scan_interval = np.linspace(self.setpoint_min, self.setpoint_max, self.setpoint_count)
        self.time_interval = np.linspace(0,(self.step_size+9)*(self.scope_count-1)/1.0e3,self.scope_count)

        self.set_dataset('set_points', ([0] * (self.scan_count * self.setpoint_count)),broadcast=True)
        self.set_dataset('act_freqs', ([0] * (self.scan_count * self.setpoint_count)),broadcast=True)
        self.set_dataset('freqs',      (self.scan_interval),broadcast=True)
        self.set_dataset('times',      (self.time_interval),broadcast=True)

        self.set_dataset('in_cell_spectrum', ([0] * self.setpoint_count),broadcast=True)
        self.set_dataset('pmt_spectrum',     ([0] * self.setpoint_count),broadcast=True)
        
        self.set_dataset('ch0_arr',  ([[0] * len(self.time_interval)] * self.scan_count * self.setpoint_count),broadcast=True)
        self.set_dataset('ch1_arr',  ([[0] * len(self.time_interval)] * self.scan_count * self.setpoint_count),broadcast=True)
        self.set_dataset('ch2_arr',  ([[0] * len(self.time_interval)] * self.scan_count * self.setpoint_count),broadcast=True)
        self.set_dataset('ch3_arr',  ([[0] * len(self.time_interval)] * self.scan_count * self.setpoint_count),broadcast=True)
        self.set_dataset('ch4_arr',  ([[0] * len(self.time_interval)] * self.scan_count * self.setpoint_count),broadcast=True)

        self.data_to_save = [{'var' : 'set_points', 'name' : 'set_points'},
                             {'var' : 'act_freqs', 'name' : 'actual frequencies (wavemeter)'},
                             {'var' : 'freqs', 'name' : 'freqs'},
                             {'var' : 'times', 'name' : 'times'},
                             {'var' : 'ch0_arr', 'name' : self.smp_data_sets['ch0']},
                             {'var' : 'ch1_arr', 'name' : self.smp_data_sets['ch1']},
                             {'var' : 'ch2_arr', 'name' : self.smp_data_sets['ch2']},
                             {'var' : 'ch3_arr', 'name' : self.smp_data_sets['ch3']},
                             {'var' : 'ch4_arr', 'name' : self.smp_data_sets['ch4']},
                             ]

        # save sequence file name
        self.config_dict.append({'par' : 'sequence_file', 'val' : os.path.abspath(__file__), 'cmt' : 'Filename of the main sequence file'})

        for k in range(5):
            print("")
        print("*"*100)
        print("* Starting new scan")
        print("*"*100)
        print("")
        print("")

        # Initializes Artiq (required)
        # get the filename for the scan, e.g. 20190618_105557
        get_basefilename(self)
        # save the config
        save_config(self.basefilename, self.config_dict)
        self.core.reset() 

    def analyze(self):
        # function is run after the experiment, i.e. after run() is called
        print('Saving data ...')
        save_all_data(self)

        # overwrite config file with complete configuration
        self.config_dict.append({'par' : 'Status', 'val' : True, 'cmt' : 'Run finished.'})
        save_config(self.basefilename, self.config_dict)

        print('Scan ' + self.basefilename + ' finished.')
        print('Scan finished.')

    def check_shot(self):
        repeat_shot = False

        # check if Yag has fired
        if self.yag_check and np.max(self.smp_data['fire_check']) < 0.3:
            repeat_shot = True
            print('No Yag')

        # check if spectroscopy light was there
        blue_min = splr.adc_mu_to_volt(40)
        if self.blue_check and np.min(self.smp_data['spec_check']) < blue_min:
            repeat_shot = True
            print('No spectroscopy')

        return repeat_shot

    def readout_data(self):
        # readout data from Artiq by toggling through all channels and saving the data in a list
        self.smp_data = {}
        for channel in self.smp_data_sets.keys():
            # self.smp_data['absorption'] = ...
            self.smp_data[self.smp_data_sets[channel]] = np.array(list(map(lambda v : splr.adc_mu_to_volt(v), self.get_dataset(channel))))

        # read laser frequencies
        self.wavemeter_frequencies = get_laser_frequencies()

    def average_data(self, first_avg = True):
        # toggle through all channels and average the data
        for channel in self.smp_data_sets.keys():
            
            # needs slices for each channel
            ind_1 = int(self.slice_min * 1e3/self.step_size)
            ind_2 = int(self.slice_max * 1e3/self.step_size)
        
            # self.smp_data['pmt_spectrum'] = ...                            
            ds = self.smp_data[self.smp_data_sets[channel]]
        
            if first_avg:
                self.smp_data_avg[self.smp_data_sets[channel]]  = np.sum(ds[ind_1:ind_2])
            else:
                self.smp_data_avg[self.smp_data_sets[channel]] += np.sum(ds[ind_1:ind_2])
               
    def update_data(self, counter, n, slowing_data = False):
        # this updates the gui for every shot
        self.mutate_dataset('set_points', counter, self.current_setpoint)
        self.mutate_dataset('act_freqs', counter, self.wavemeter_frequencies)
        self.mutate_dataset('in_cell_spectrum', n, self.smp_data_avg['absorption'])
        self.mutate_dataset('pmt_spectrum',     n, self.smp_data_avg['pmt'])
        
        # save each successful shot in ch<number>_arr datasets
        # needs fixing since the number of channels is hardcoded here
        for k in range(5):
            slice_ind = (counter)
            hlp_data = self.smp_data[self.smp_data_sets['ch' + str(k)]]
        
            self.mutate_dataset('ch' + str(k) + '_arr', slice_ind, hlp_data)

    def set_single_laser(self, my_file, freq):
        setpoint_file = open(my_file, 'w')
        setpoint_file.write(str(freq))
        setpoint_file.close()

    def set_lasers(self, nu = 0.0, init = False):

        if init:
            # set lasers to starting points of the scan and to their initial values
            nu = np.min(self.scan_interval)

            if  self.which_scanning_laser == 1:
                self.current_setpoint = nu #self.offset_laser1 + nu/1.0e6
                self.set_single_laser(self.setpoint_filename_laser1, self.offset_laser1 + nu/1.0e6)
                self.set_single_laser(self.setpoint_filename_laser2, self.offset_laser2)

            elif  self.which_scanning_laser == 2:
                self.current_setpoint = nu #self.offset_laser2 + nu/1.0e6
                self.set_single_laser(self.setpoint_filename_laser1, self.offset_laser1)
                self.set_single_laser(self.setpoint_filename_laser2, self.offset_laser2 + nu/1.0e6)

        else:

            if  self.which_scanning_laser == 1:
                self.current_setpoint = nu #self.offset_laser1 + nu/1.0e6
                self.set_single_laser(self.setpoint_filename_laser1, self.offset_laser1 + nu/1.0e6)

            elif  self.which_scanning_laser == 2:
                self.current_setpoint = nu #self.offset_laser2 + nu/1.0e6
                self.set_single_laser(self.setpoint_filename_laser2, self.offset_laser2 + nu/1.0e6)



    def run(self):

        # init lasers
        self.set_lasers(init = True)
       
        # pause to wait till laser settles
        time.sleep(1)

        counter = 0
        # loop over setpoints
        for n, nu in enumerate(self.scan_interval): 

            self.set_lasers(nu)

            print(str(n+1) + ' / ' + str(self.setpoint_count) + ' setpoints')

            if n == 0:
                time.sleep(0.1)
            else:
                time.sleep(0.1)

            self.smp_data_avg = {}
            # loop over averages
            for i_avg in range(self.scan_count):                
                print(str(i_avg+1) + ' / ' + str(self.scan_count) + ' averages')
                self.scheduler.pause()                
              
                repeat_shot = True
                while repeat_shot:
                    
                    # fires yag and reads voltages
                    self.fire_and_read()

                    # readout the data
                    self.readout_data()

                    repeat_shot = self.check_shot()
                    if repeat_shot == False:                        
                        # upon success add data to dataset
                        self.average_data(first_avg = (i_avg == 0))
                        
                        self.update_data(counter, n)

                        counter += 1
                    
                    time.sleep(self.repetition_time)

            print()
            print()


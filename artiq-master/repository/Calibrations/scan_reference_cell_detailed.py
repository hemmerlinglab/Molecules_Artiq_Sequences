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
from rubidium_lines import get_rb_scan_interval


# every Experiment needs a build and a run function
class Scan_Reference_Cell_Detailed(EnvExperiment):
    def build(self):

        self.config_dict = []
        self.wavemeter_frequencies = []
        
        self.setattr_device('core') # Core Artiq Device (required)
        self.setattr_device('ttl9') # experimental start

        self.setattr_device('sampler1') # adc voltage sampler
        self.setattr_device('scheduler') # scheduler used
        
        # EnvExperiment attribute: number of voltage samples per scan
        self.my_setattr('scope_count',NumberValue(default=400,unit='reads per shot',scale=1,ndecimals=0,step=1))
        self.my_setattr('scan_count',NumberValue(default=2,unit='averages',scale=1,ndecimals=0,step=1))
        #self.my_setattr('setpoint_offset',NumberValue(default=384.23,unit='THz',scale=1,ndecimals=6,step=.000001))
        self.my_setattr('setpoint_offset',NumberValue(default=377.107,unit='THz',scale=1,ndecimals=6,step=.000001))
        #self.my_setattr('setpoint_min',NumberValue(default=-3000,unit='MHz',scale=1,ndecimals=0,step=1))
        #self.my_setattr('setpoint_max',NumberValue(default=3000,unit='MHz',scale=1,ndecimals=0,step=1))
        self.my_setattr('df',NumberValue(default=40.0,unit='MHz',scale=1,ndecimals=6,step=.000001))
        self.my_setattr('no_of_points',NumberValue(default=20,unit='',scale=1,ndecimals=1,step=1))

        self.my_setattr('step_size',NumberValue(default=100,unit='us',scale=1,ndecimals=0,step=1))
        self.my_setattr('slice_min',NumberValue(default=0,unit='ms',scale=1,ndecimals=1,step=0.1))
        self.my_setattr('slice_max',NumberValue(default=40,unit='ms',scale=1,ndecimals=1,step=0.1))

        self.my_setattr('repetition_time',NumberValue(default=0.1,unit='s',scale=1,ndecimals=1,step=0.1))
        
        #self.my_setattr('setpoint_count',NumberValue(default=len(self.scan_interval),unit='setpoints',scale=1,ndecimals=0,step=1))

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
    @kernel
    def fire_and_read(self):
        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        self.sampler1.init() # initializes sampler device
        
        ### Set Channel Gain 
        for i in range(8):
            self.sampler1.set_gain_mu(i,0) # (channel,setting) gain is 10^setting
        
        delay(260*us)
        
        ### Data Variable Initialization
        data0 = [0]*self.scope_count # data0
        data1 = [0]*self.scope_count # data2
        data2 = [0]*self.scope_count # data2
        smp = [0]*8 # individual sample

        ### Fire and sample
        with parallel:
            
            with sequential:
                self.ttl9.pulse(10*us) # experimental start

            with sequential:
                for j in range(self.scope_count):
                    self.sampler1.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
                    data0[j] = smp[0]
                    data1[j] = smp[1]
                    data2[j] = smp[2]
                    #delay(5*us)
                    delay(self.step_size*us) # plus 9us from sample_mu

        ### Allocate and Transmit Data All Channels
        self.set_dataset('ch0', (data0), broadcast = True)
        self.set_dataset('ch1', (data1), broadcast = True)
        self.set_dataset('ch2', (data2), broadcast = True)


    def prepare(self):
        # function is run before the experiment, i.e. before run() is called

        self.smp_data_sets = {
                'ch0' : 'absorption0',
                'ch1' : 'absorption1',
                'ch2' : 'reference'
                }
        self.scan_interval = get_rb_scan_interval(no_of_points = self.no_of_points, df = self.df, cnt_freq = self.setpoint_offset*1e12) #np.linspace(self.setpoint_min, self.setpoint_max, self.setpoint_count)

        self.setpoint_count = len(self.scan_interval)

        self.time_interval = np.linspace(0,(self.step_size+9)*(self.scope_count-1)/1.0e3,self.scope_count)
        
        self.set_dataset('set_points', ([0] * (self.scan_count * self.setpoint_count)),broadcast=True)
        self.set_dataset('act_freqs', ([0] * (self.scan_count * self.setpoint_count)),broadcast=True)
        self.set_dataset('freqs',      (self.scan_interval),broadcast=True)
        self.set_dataset('times',      (self.time_interval),broadcast=True)

        self.set_dataset('abs_spec0', ([0] * self.setpoint_count),broadcast=True)
        self.set_dataset('abs_spec1', ([0] * self.setpoint_count),broadcast=True)
        self.set_dataset('reference', ([0] * self.setpoint_count),broadcast=True)
        self.set_dataset('diff_spec', ([0] * self.setpoint_count),broadcast=True)

        self.set_dataset('ch0_arr',  ([[0] * len(self.time_interval)] * self.scan_count * self.setpoint_count),broadcast=True)
        self.set_dataset('ch1_arr',  ([[0] * len(self.time_interval)] * self.scan_count * self.setpoint_count),broadcast=True)
        self.set_dataset('ch2_arr',  ([[0] * len(self.time_interval)] * self.scan_count * self.setpoint_count),broadcast=True)

        self.data_to_save = [{'var' : 'set_points', 'name' : 'set_points'},
                             {'var' : 'act_freqs', 'name' : 'actual frequencies (wavemeter)'},
                             {'var' : 'freqs', 'name' : 'freqs'},
                             {'var' : 'times', 'name' : 'times'},
                             {'var' : 'ch0_arr', 'name' : self.smp_data_sets['ch0']},
                             {'var' : 'ch1_arr', 'name' : self.smp_data_sets['ch1']},
                             {'var' : 'ch2_arr', 'name' : self.smp_data_sets['ch2']}
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
        self.mutate_dataset('abs_spec0', n, self.smp_data_avg['absorption0'])
        self.mutate_dataset('abs_spec1', n, self.smp_data_avg['absorption1'])
        self.mutate_dataset('diff_spec', n, self.smp_data_avg['absorption1'] - self.smp_data_avg['absorption0'])
        
        # save each successful shot in ch<number>_arr datasets
        # needs fixing since the number of channels is hardcoded here
        for k in range(3):
            slice_ind = (counter)
            hlp_data = self.smp_data[self.smp_data_sets['ch' + str(k)]]
        
            self.mutate_dataset('ch' + str(k) + '_arr', slice_ind, hlp_data)

    def run(self):

        last_nu = 0.0
        counter = 0
        # loop over setpoints
        for n, nu in enumerate(self.scan_interval): 

            print(str(n+1) + ' / ' + str(self.setpoint_count) + ' setpoints')
            self.current_setpoint = nu

            # move laser to set point
            setpoint_file = open(self.setpoint_filename_laser2, 'w')
            setpoint_file.write(str(self.setpoint_offset + nu/1.0e6))
            setpoint_file.close()

            if np.abs(last_nu - nu) > 20:
                # if jump to next frequency is larger than 20 MHz, give laser time to lock
                print('Waiting for laser to lock ...')
                time.sleep(5)
            else:
                time.sleep(self.repetition_time)
            last_nu = nu

            hlp_counter = counter
            # take self.scan_count averages with slowing laser and then the same without

            # reset counter to accommodate for the slow on/slow off sequence
            counter = hlp_counter

            self.smp_data_avg = {}
            # loop over averages
            for i_avg in range(self.scan_count):                
                    print(str(i_avg+1) + ' / ' + str(self.scan_count) + ' averages')
                    self.scheduler.pause()                
                  
                    self.fire_and_read()

                    # readout the data
                    self.readout_data()
    
                    self.average_data(first_avg = (i_avg == 0))
                            
                    self.update_data(counter, n)
    
                    counter += 1
                        

            print()
            print()


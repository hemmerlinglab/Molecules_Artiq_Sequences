# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime
import os
import time
import csv

from helper_functions import *


# every Experiment needs a build and a run function
class Shutter_Test(EnvExperiment):
    def build(self):
        self.setattr_device('core') # Core Artiq Device (required)
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('ttl5') # uv ccd trigger
        self.setattr_device('ttl8') # slowing shutter
        self.setattr_device('ttl9') # experimental start

        self.setattr_device('sampler0') # adc voltage sampler
        self.setattr_device('scheduler') # scheduler used
        # EnvExperiment attribute: number of voltage samples per scan
        self.setattr_argument('scope_count',NumberValue(default=400,unit='reads per shot',scale=1,ndecimals=0,step=1))
        self.setattr_argument('scan_count',NumberValue(default=2,unit='averages',scale=1,ndecimals=0,step=1))
        self.setattr_argument('setpoint_count',NumberValue(default=100,unit='setpoints',scale=1,ndecimals=0,step=1))
        self.setattr_argument('setpoint_offset',NumberValue(default=375.763266,unit='THz',scale=1,ndecimals=6,step=.000001))
        self.setattr_argument('setpoint_min',NumberValue(default=-750,unit='MHz',scale=1,ndecimals=0,step=1))
        self.setattr_argument('setpoint_max',NumberValue(default=1500,unit='MHz',scale=1,ndecimals=0,step=1))
        self.setattr_argument('slowing_set',NumberValue(default = 375.763,unit='THz',scale=1,ndecimals=6,step=.000001))
        self.setattr_argument('slow_start',NumberValue(default=0,unit='ms',scale=1,ndecimals=2,step=0.01))
        self.setattr_argument('slow_stop',NumberValue(default=2,unit='ms',scale=1,ndecimals=2,step=0.01))

        self.setattr_argument('step_size',NumberValue(default=60,unit='us',scale=1,ndecimals=0,step=1))
        self.setattr_argument('slice_min',NumberValue(default=5,unit='ms',scale=1,ndecimals=1,step=0.1))
        self.setattr_argument('slice_max',NumberValue(default=6,unit='ms',scale=1,ndecimals=1,step=0.1))
        self.setattr_argument('pmt_slice_min',NumberValue(default=5,unit='ms',scale=1,ndecimals=1,step=0.1))
        self.setattr_argument('pmt_slice_max',NumberValue(default=6,unit='ms',scale=1,ndecimals=1,step=0.1))
          
        self.setattr_argument('yag_power',NumberValue(default=5,unit='',scale=1,ndecimals=1,step=0.1))
        self.setattr_argument('he_flow',NumberValue(default=3,unit='sccm',scale=1,ndecimals=1,step=0.1))
        self.setattr_argument('yag_check',BooleanValue())
        self.setattr_argument('blue_check',BooleanValue())

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

                delay(150*us)
                self.ttl4.pulse(15*us) # trigger flash lamp
                delay(135*us) # wait optimal time (see Minilite manual)
                self.ttl6.pulse(15*us) # trigger q-switch
                delay(100*us) # wait until some time after green flash
                self.ttl5.pulse(15*us) # trigger uv ccd

            with sequential:
                # slowing pulse
                self.ttl8.on() # shutter on
                delay(4500*us)
                self.ttl8.off()
                delay(4400*us)
                self.ttl8.on()

                # should move this end of sequence
                delay(20000*us)
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
        # https://m-labs.hk/artiq/manual/core_language_reference.html#module-artiq.language.environment
        my_today = datetime.datetime.today()

        datafolder = '/home/molecules/software/data/'
        setpoint_filename = '/home/molecules/skynet/Logs/setpoint.txt'

        basefolder = str(my_today.strftime('%Y%m%d')) # 20190618
        # create new folder if doesn't exist yet
        if not os.path.exists(datafolder + basefolder):
            os.makedirs(datafolder + basefolder)

        self.basefilename = datafolder + basefolder + '/' + str(my_today.strftime('%Y%m%d_%H%M%S')) # 20190618_105557

     
        self.smp_data_sets = {
                'ch0' : 'absorption',
                'ch1' : 'fire_check',
                'ch2' : 'pmt',
                'ch3' : 'spec_check',
                'ch4' : 'slow_check'
                }

        self.scan_interval = np.linspace(self.setpoint_min, self.setpoint_max, self.setpoint_count)

        self.set_dataset('set_points', ([0] * (self.scan_count * self.setpoints_count)),broadcast=True)
        self.set_dataset('freqs',      (self.scan_interval),broadcast=True)
        self.set_dataset('times',      (np.linspace(0,(self.step_size+9)*(self.scope_count-1)/1.0e3,self.scope_count)),broadcast=True)

        self.set_dataset('in_cell_spectrum', ([0] * self.setpoint_count),broadcast=True)
        self.set_dataset('pmt_spectrum',     ([0] * self.setpoint_count),broadcast=True)
     

        # how can we get all arguments?
        # save run configuration
        self.config_dict = [
                {'par' : 'scope_count', 'val' : self.scope_count, 'cmt' : 'Number of samples per shot'},
                {'par' : 'scan_count', 'val' : self.scan_count, 'cmt' : 'Number of averages'},
                {'par' : 'step_size', 'val' : self.step_size, 'cmt' : 'Step size'},
                {'par' : 'set_point_count', 'val' : self.setpoint_count, 'cmt' : 'Step size'},
                {'par' : 'he_flow', 'val' : self.he_flow, 'unit' : 'sccm', 'cmt' : 'He flow'},
                {'par' : 'yag_power', 'val' : self.yag_power, 'cmt' : 'He flow'},
                {'par' : 'min_x', 'val' : self.min_x, 'cmt' : 'min x'},
                {'par' : 'min_y', 'val' : self.min_y, 'cmt' : 'min y'},
                {'par' : 'max_x', 'val' : self.max_x, 'cmt' : 'max x'},
                {'par' : 'max_y', 'val' : self.max_y, 'cmt' : 'max y'},
                {'par' : 'steps_x', 'val' : self.steps_x, 'cmt' : 'steps x'},
                {'par' : 'steps_y', 'val' : self.steps_y, 'cmt' : 'steps y'},
                {'par' : 'yag_power', 'val' : self.yag_power, 'cmt' : 'He flow'},
                {'par' : 'yag_check', 'val' : self.yag_check, 'cmt' : 'Yag check'},
                {'par' : 'blue_check', 'val' : self.blue_check, 'cmt' : 'Blue check'},
                {'par' : 'data_sets', 'val' : self.smp_data_sets, 'cmt' : 'Data sets'}
                ]

        for k in range(5):
            print("")
        print("*"*100)
        print("* Starting new scan")
        print("*"*100)
        print("")
        print("")

        # Initializes Artiq (required)
        save_config(self.basefilename, self.config_dict)
        self.core.reset() 

    def analyze(self):
        # function is run after the experiment, i.e. after run() is called
        print('Saving data ...')
        save_all_data(self.basefilename,
                [{'var' : self.get_dataset('set_points'), 'name' : 'Set points'},
                 {'var' : self.get_dataset('freqs'), 'name' : 'Frequencies interval'},
                 {'var' : self.get_dataset('times'), 'name' : 'Times'},
                 {'var' : self.get_dataset('ch0'), 'name' : self.smp_data_sets['ch0']},
                 {'var' : self.get_dataset('ch1'), 'name' : self.smp_data_sets['ch1']},
                 {'var' : self.get_dataset('ch2'), 'name' : self.smp_data_sets['ch2']},
                 {'var' : self.get_dataset('ch3'), 'name' : self.smp_data_sets['ch3']},
                 {'var' : self.get_dataset('ch4'), 'name' : self.smp_data_sets['ch4']}
                 ])

        # overwrite config file with complete configuration
        self.config_dict.append({'par' : 'Status', 'val' : True, 'cmt' : 'Run finished.'})
        save_config(self.basefilename, self.config_dict)

        print('Scan ' + self.basefilename + ' finished.')

        print('Scan finished.')

    def check_shot(self):
        repeat_shot = False

        # check if Yag has fired
        if np.max(self.smp_data['fire_check']) < 0.3:
            repeat_shot = True
            print('No Yag')

        # check if spectroscopy light was there
        blue_min = splr.adc_mu_to_volt(40)
        if np.min(self.smp_data['spec_check']) < blue_min:
            repeat_shot = True
            print('No spectroscopy')

        # check if slowing light was there
        blue_min = splr.adc_mu_to_volt(40)
        if np.min(self.smp_data['slow_check']) < blue_min:
            repeat_shot = True
            print('No slowing')

        return repeat_shot

    def run(self):

        counter = 0
        # loop over setpoints
        for n, nu in enumerate(self.scan_interval): 

            print(str(n) + ' / ' + str(self.setpoint_count))

            self.smp_data_avg = {}
            # loop over averages
            for i_avg in range(self.scan_count):                
                self.scheduler.pause()                
              
                repeat_shot = False
                while repeat_shot:
                    
                    # fires yag and reads voltages
                    self.fire_and_read()

                    # readout data from Artiq by toggling through all channels and saving the data in a list
                    self.smp_data = {}
                    for channel in self.smp_data_sets.keys():
                        # self.smp_data['absorption'] = ...
                        self.smp_data[self.smp_data_sets[channel]] = np.array(list(map(lambda v : splr.adc_mu_to_volt(v), self.get_dataset(channel))))


                    repeat_shot = self.check_shot()
                    if repeat_shot == False:                        
                        # upon success add data to dataset
                        counter += 1

                        # toggle through all channels and average the data
                        for channel in self.smp_data_sets.keys():
                            # self.smp_data['pmt_spectrum'] = ...
                            
                            ds = self.smp_data[self.smp_data_sets[channel]]

                            # needs slices for each channel
                            ind_1 = int(self.slice_min * 1e3/self.step_size)
                            ind_2 = int(self.slice_max * 1e3/self.step_size)

                            if i_avg == 0:
                                self.smp_data_avg[self.smp_data_sets[channel]  = np.sum(ds[ind_1:ind_2)])
                            else:
                                self.smp_data_avg[self.smp_data_sets[channel] += np.sum(ds[ind_1:ind_2)])
                                            
                        self.mutate_dataset('set_points', counter, nu)
                        self.mutate_dataset('in_cell_spectrum', n, self.smp_data_avg['absorption'])
                        self.mutate_dataset('pmt_spectrum',     n, self.smp_data_avg['pmt'])
                    
                    time.sleep(0.2)

            print()
            print()


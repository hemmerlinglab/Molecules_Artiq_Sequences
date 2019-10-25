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

                # should move to end of sequence
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

        
        ### Allocate and Transmit Data
        self.set_dataset('absorption', (data0), broadcast = True)
        self.set_dataset('fire_check', (data1), broadcast = True)
        self.set_dataset('pmt',        (data2), broadcast = True)
        self.set_dataset('spec_check', (data3), broadcast = True)
        self.set_dataset('slow_check', (data4), broadcast = True)

    def prepare(self):
        # function is run before the experiment, i.e. before run() is called
        # https://m-labs.hk/artiq/manual/core_language_reference.html#module-artiq.language.environment

        self.smp_data_sets = ['absorption', 'fire_check', 'pmt', 'spec_check', 'slow_check']

        self.smp_data = {}

        for k in range(5):
            print("")
        print("*"*100)
        print("* Starting new scan")
        print("*"*100)
        print("")
        print("")

    def analyze(self):
        # function is run after the experiment, i.e. after run() is called

        print('Scan finished.')

    def run(self):
        ### Initializations
        self.core.reset() # Initializes Artiq (required)

        set_freqs = [] # absorption signal
        volts = [] # absorption signal
        frchks = [] # yag fire check
        fluor = [] # fluorescence pmt signal
        postsel = [] # spec blue post select
        postsel2 = [] # slow blue post select

        avgs = [0]*self.setpoint_count
        pmt_avgs = [0]*self.setpoint_count
        
        scan_interval = np.linspace(self.setpoint_min,self.setpoint_max,self.setpoint_count)

        self.set_dataset('freqs',(scan_interval),broadcast=True)
        self.set_dataset('times',(np.linspace(0,(self.step_size+9)*(self.scope_count-1)/1e3,self.scope_count)),broadcast=True)

        self.set_dataset('spectrum',(avgs),broadcast=True)
        self.set_dataset('pmt_spectrum',(pmt_avgs),broadcast=True)
        
        for n, nu in enumerate(scan_interval): 

            print(str(n) + ' / ' + str(self.setpoint_count))

            new_avg = 0
            new_avg_pmt = 0

            # run scan_count averages
        
            ### Run Experiment
            for i in range(self.scan_count):
                self.scheduler.pause()
               
                #while not shot_fired and not blue_on and not slow_on:
                if True:
                    #break  #break will break out of the infinite while loop
    #                input('Press ENTER for Run {}/{}'.format(i+1,scan_count))
                    self.fire_and_read() # fires yag and reads voltages

                    for d_n, data_set in enumerate(self.smp_data_sets):
                        self.smp_data[data_set] = list(map(lambda v : splr.adc_mu_to_volt(v), self.get_dataset(data_set)))


                    set_freqs.append(nu)

                    new_avg += sum(self.smp_data['absorption'][int(self.slice_min*1e3/self.step_size):int(self.slice_max*1e3/self.step_size)])
                    new_avg_pmt += sum(self.smp_data['pmt'][int(self.pmt_slice_min*1e3/self.step_size):int(self.pmt_slice_max*1e3/self.step_size)])

                    ## check if Yag fired
                    #if np.max(np.array(hlp2)) > 0.0:
                    #    # save set points for each shot
                    #    if np.min(np.array(hlp4)) > 0.0:#blue_min:
                    #        if np.min(np.array(hlp5)) > 0.0:#slow_min:
                    #            volts.append(hlp)
                    #            frchks.append(hlp2)
                    #            fluor.append(hlp3)
                    #            postsel.append(hlp4)
                    #            postsel2.append(hlp5)
                    #            new_avg = new_avg + sum(hlp[int(self.slice_min*1e3/self.step_size):int(self.slice_max*1e3/self.step_size)])
                    #            new_avg_pmt = new_avg_pmt + sum(hlp3[int(self.pmt_slice_min*1e3/self.step_size):int(self.pmt_slice_max*1e3/self.step_size)])

                    #            print('Scan {}/{} Completed'.format(i+1,self.scan_count))
                    #            shot_fired = True
                    #            blue_on = True
                    #            slow_on = True
                    #        else:
                    #            slow_on = False
                    #            print('Repeat shot. No Slow Blue.')
                    #    else:
                    #        blue_on = False
                    #        print('Repeat shot. No Spec Blue.')
                    #else:
                    #    #break
                    #    # repeat shot
                    #    shot_fired = False
                    #    print('Repeat shot. No Yag.')
                
                    time.sleep(0.2)

            #new_avg = new_avg/self.scan_count
            self.mutate_dataset('spectrum',n,new_avg)
            self.mutate_dataset('pmt_spectrum',n,new_avg_pmt)

            print()
            print()


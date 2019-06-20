# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime
import os
import time
import csv

# every Experiment needs a build and a run function
class DAQ(EnvExperiment):
    def build(self):
        self.setattr_device('core') # Core Artiq Device (required)
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('sampler0') # adc voltage sampler
        # EnvExperiment attribute: number of voltage samples per scan
        self.setattr_argument('scope_count',NumberValue(default=600,ndecimals=0,step=1))
 
    ### Script to run on Artiq
    # Basic Schedule:
    # 1) Trigger YAG Flashlamp
    # 2) Wait 150 us
    # 3) Trigger Q Switch
    # 4) In parallel, read off 2 diodes
    @kernel
    def fire_and_read(self):
        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        self.sampler0.init() # initializes sampler device
        
        ### Set Channel Gain 
        for i in range(8):
            self.sampler0.set_gain_mu(i,0) # (channel,setting) gain is 10^setting
        
        delay(100*us)
        
        ### Data Variable Initialization
        data0 = [0]*self.scope_count # signal data
        data1 = [0]*self.scope_count # fire check data
        smp = [0]*8 # individual sample

        ### Fire and sample
        self.ttl4.pulse(15*us) # trigger flash lamp
        delay(135*us) # wait optimal time (see Minilite manual)
        self.ttl6.pulse(15*us) # trigger q-switch
        for j in range(self.scope_count):
            self.sampler0.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
            data0[j] = smp[0]
            data1[j] = smp[1]
            #delay(5*us)
            delay(50*us)
            
        ### Allocate and Transmit Data
        index = range(self.scope_count)
        self.mutate_dataset('absorption',index,data0)
        self.mutate_dataset('fire_check',index,data1)

    def run(self):
        ### Initilizations
        self.core.reset() # Initializes Artiq (required)
        self.set_dataset('absorption',np.full(self.scope_count,np.nan)) # class dataset for Artiq communication
        self.set_dataset('fire_check',np.full(self.scope_count,np.nan)) # class dataset for Artiq communication

        set_freqs = [] # absorption signal
        volts = [] # absorption signal
        frchks = [] # yag fire check


        # Define scan parameters
        
        scan_count = 10 # number of loops/averages
        scan_offset = 375.763266 # THz
        no_of_points = 100

        scan_interval = 0.5 * np.linspace(-600,1500,no_of_points) * 1.0e6 # MHz
        scan_interval = scan_offset + scan_interval/1e12
  
        # End of define scan parameters



        my_today = datetime.datetime.today()

        datafolder = '/home/molecules/software/data/'
        setpoint_filename = '/home/molecules/skynet/setpoint.txt'

        basefolder = str(my_today.strftime('%Y%m%d')) # 20190618
        # create new folder if doesn't exist yet
        if not os.path.exists(datafolder + basefolder):
            os.makedirs(datafolder + basefolder)

        basefilename = datafolder + basefolder + '/' + str(my_today.strftime('%Y%m%d_%H%M%S')) # 20190618_105557

        for n, nu in enumerate(scan_interval): 
            print('-'*30)
            print('Setpoint {}/{}'.format(n+1,no_of_points))
            print('Setting laser to ' + str(nu))

            # move laser to set point
            setpoint_file = open(setpoint_filename, 'w')
            setpoint_file.write(str(nu))
            setpoint_file.close()

            time.sleep(2.0)

            # run scan_count averages
        
            ### Run Experiment
            for i in range(scan_count):

                shot_fired = False

                while not shot_fired:
    #                input('Press ENTER for Run {}/{}'.format(i+1,scan_count))
                    self.fire_and_read() # fires yag and reads voltages
                    vals = self.get_dataset('absorption')
                    chks = self.get_dataset('fire_check')

                    hlp = []
                    for v in vals:
                        hlp.append(splr.adc_mu_to_volt(v))

                    hlp2 = []
                    for f in chks:
                        hlp2.append(splr.adc_mu_to_volt(f))

                    # check if Yag fired
                    if np.max(np.array(hlp2)) > 0.5:
                        # save set points for each shot
                        set_freqs.append(nu)
                        volts.append(hlp)
                        frchks.append(hlp2)
    
                        print('Run {}/{} Completed'.format(i+1,scan_count))
                        shot_fired = True
                    else:
                        # repeat shot
                        shot_fired = False
                        print('Repeat shot. No Yag.')
                
                    time.sleep(1.0)

        # transform into numpy arrays                
        freqs = np.array(set_freqs)
        ch1 = np.array(volts)
        ch2 = np.array(frchks)

        print(freqs)

        print('Saving data ...')
        ### Write Data to Files
        f_freqs = open(basefilename + '_freqs','w')
        f_ch1 = open(basefilename + '_ch1','w')
        f_ch2 = open(basefilename + '_ch2','w')

        np.savetxt(f_freqs, freqs, delimiter=",")
        f_freqs.close()

        np.savetxt(f_ch1, ch1, delimiter=",")
        f_ch1.close()

        np.savetxt(f_ch2, ch2, delimiter=",")
        f_ch2.close()

        print('Filename: ' + basefilename)



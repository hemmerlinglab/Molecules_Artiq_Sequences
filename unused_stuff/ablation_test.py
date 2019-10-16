# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime

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
            delay(5*us)
            
        ### Allocate and Transmit Data
        index = range(self.scope_count)
        self.mutate_dataset('absorption',index,data0)
        self.mutate_dataset('fire_check',index,data1)

    def run(self):
        ### Initilizations
        self.core.reset() # Initializes Artiq (required)
        scan_count = 1 # number of loops
        self.set_dataset('absorption',np.full(self.scope_count,np.nan)) # class dataset for Artiq communication
        self.set_dataset('fire_check',np.full(self.scope_count,np.nan)) # class dataset for Artiq communication
        volts = [] # absorption signal
        frchks = [] # yag fire check

        ### Run Experiment
        for i in range(scan_count):
            print('loop {}'.format(i))
            #input('Press ENTER for Run {}/{}'.format(i+1,scan_count))
            self.fire_and_read() # fires yag and reads voltages
            vals = self.get_dataset('absorption')
            chks = self.get_dataset('fire_check')
            for v in vals:
                volts.append(splr.adc_mu_to_volt(v))
            for f in chks:
                frchks.append(splr.adc_mu_to_volt(f))

            
            print('Run {}/{} Completed'.format(i+1,scan_count))
       
        ### Write Data to Files
        v_name = 'signal_1.txt'
        v_out = open(v_name,'w')
        for v in volts:
            v_out.write(str(v)+' ')
        v_out.close()
        print('Absorption signal data written to {}'.format(v_name))

        f_name = 'fire_check_1.txt'
        f_out = open(f_name,'w')
        print(frchks)
        for f in frchks:
            f_out.write(str(f)+' ')
        f_out.close()
        print('Fire check data written to {}'.format(f_name))



        



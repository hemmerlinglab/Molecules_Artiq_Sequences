# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime

# every Experiment needs a build and a run function
class ABLATION_TEST(EnvExperiment):
    def build(self):
        self.setattr_device('core') # Core Artiq Device (required)
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('sampler0') # adc voltage sampler
        self.setattr_device('scheduler')
        # EnvExperiment attribute: number of voltage samples per scan
        self.setattr_argument('scope_count',NumberValue(default=400,ndecimals=0,step=1))
        self.setattr_argument('scan_count',NumberValue(default=10,ndecimals=0,step=1))
 
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
        data0 = [0]*self.scope_count # cell data
        data1 = [0]*self.scope_count # fire check data
        data2 = [0]*self.scope_count # uhv data
        smp = [0]*8 # individual sample

        ### Fire and sample
        self.ttl4.pulse(1*ms) # trigger flash lamp
        delay(15*us) # wait optimal time (see Minilite manual)
        self.ttl6.pulse(1*ms)
         # trigger q-switch
        for j in range(self.scope_count):
            self.sampler0.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
            data0[j] = smp[0]
            data1[j] = smp[1]
            data2[j] = smp[2]
            delay(15*us)  

        ### Allocate and Transmit Data
        #index = range(self.scope_count)
        self.set_dataset('absorption',(data0),broadcast=True) # class dataset for Artiq communication
        self.set_dataset('fire_check',(data1),broadcast=True) # class dataset for Artiq communication
        self.set_dataset('pmt',(data2),broadcast=True)
        #self.setattr_dataset('absorption')
        #self.setattr_dataset('fire_check')

    def run(self):
        ### Initilizations
        self.core.reset() # Initializes Artiq (required)
        ##self.scan_count = 10 # number of loops

        volts = [] # absorption signal
        frchks = [] # yag fire check
        fluor = [] # fluorescence pmt signal
        avgs = [0]*self.scan_count

        ### Run Experiment
        for i in range(self.scan_count):
            self.scheduler.pause()
            #input('Press ENTER for Run {}/{}'.format(i+1,scan_count))
            self.fire_and_read() # fires yag and reads voltages
            vals = self.get_dataset('absorption')
            chks = self.get_dataset('fire_check')
            pmts = self.get_dataset('pmt')
            new_volts = []
            #print(vals)
            #print(frchks)
            for v in vals:
                new_volts = [splr.adc_mu_to_volt(v)]
                volts = volts + new_volts
            for f in chks:
                frchks = frchks + [splr.adc_mu_to_volt(f)]
            for p in pmts:
                fluor = fluor + [splr.adc_mu_to_volt(p)]

            avgs[i] = sum(new_volts)
            self.set_dataset('signal',(avgs),broadcast=True)

            
            print('Run {}/{} Completed'.format(i+1,self.scan_count))
       
        ## Write Data to Files
        v_name = 'signal_1.txt'
        v_out = open(v_name,'w')
        for v in volts:
            v_out.write(str(v)+' ')
        v_out.close()
        print('Absorption signal data written to {}'.format(v_name))

        f_name = 'fire_check_1.txt'
        f_out = open(f_name,'w')
        #print(frchks)
        for f in frchks:
            f_out.write(str(f)+' ')
        f_out.close()
        print('Fire check data written to {}'.format(f_name))

        p_name = 'pmt_1.txt'
        p_out = open(p_name,'w')
        for p in fluor:
            p_out.write(str(p)+' ')
        p_out.close()
        print('PMT check data written to {}'.format(p_name))




        



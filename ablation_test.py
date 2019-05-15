# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime

# every Experiment needs a build and a run function
class DAQ(EnvExperiment):
    def build(self):
        self.setattr_device('core')
        self.setattr_device('ttl11') # experiment start
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('sampler0')
        self.setattr_argument('scope_count',NumberValue(default=600,ndecimals=0,step=1))
        self.setattr_argument('scan_count',NumberValue(default=1,ndecimals=0,step=1))

    """ Tells it to run at the core device, @ kernel is necessary to run the process entirely in artiq's core
    Notes: 
    - any command that needs to talk to the computer severely slows down (or makes it not work) the process because its not in artiq's processer
    - normal python commands such as print and plotting figures slows the kernel, or will make it not work"""
    @kernel
    def fire_and_read(self):
        self.core.break_realtime()
        self.sampler0.init()
        
        """ 
         This function sets the gain for each sampler channel
         * i iterates over 8 adc channels
         * gain is 10^(input setting), which is the second number in the set_gain_mu()
         --> currently has a gain of 1 """    
        for i in range(8):
            self.sampler0.set_gain_mu(i,0)
        
        # initilization, sets up the array of zeros of values to be replaced
        data = [0]*self.scope_count
        smp = [0]*8 # array of numbers coming from each sampler port
        
        ### Fire and sample
        self.ttl4.pulse(15*us) # trigger flash lamp
        delay(150*us) # wait optimal time
        self.ttl6.pulse(15*us) # trigger q-switch
        for j in range(self.scope_count):
            delay(3.3*us) # needed to prevent underflow errors
            self.sampler0.sample_mu(smp) # reads out into smp which takes data from all 8 ports
            data[j] = smp[0] # replaces the value at specified data[j] with the updated scalar from smp[0] (channel 0 of the sampler ports)  
            
            
        index = range(self.scope_count)
        self.mutate_dataset('scope_read',index,data)

    def run(self):
        self.core.reset()
        x = np.arange(self.scope_count)
        self.set_dataset('scope_read',np.full(self.scope_count,np.nan))
        for i in range(self.scan_count):
            input('Press ENTER for Run {}/{}'.format(i+1,self.scan_count))
            self.fire_and_read()
            print('Run {}/{} Completed'.format(i+1,self.scan_count))

        vals = self.get_dataset('scope_read')
        volts = []
        for v in vals:
            volts.append(splr.adc_mu_to_volt(v))
        f_name = 'test3.txt'
        f_out = open(f_name,'w')
        for v in volts:
            f_out.write(str(v)+' ')
        f_out.close()
        print('Voltage data written to {}'.format(f_name))



        



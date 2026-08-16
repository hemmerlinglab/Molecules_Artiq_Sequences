from artiq.experiment import *
from artiq.language.types import TBool, TFloat, TInt32, TInt64, TList, TTuple
from artiq.coredevice import ad9910


import numpy as np



class DDS_RAM(EnvExperiment):
    
    def build(self):
        # 1. Initialize core device
        self.setattr_device("core")
        
        ## 2. Bind the DDS channel (e.g., AD9910 or AD9914)
        #self.setattr_device("urukul0_ch0")

        #self.setattr_argument('frequency', NumberValue(default = 10, unit='MHz', min=1.0, max = 800.0, scale=1,ndecimals=1,step=1))

        self.dds = self.get_device("urukul0_ch0")  # Set specific channel
        self.cpld = self.get_device("urukul0_cpld")

        self.setattr_device('ttl16')

        self.amp = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
        self.asf_ram = [0] * len(self.amp)

    @kernel
    def run(self):
        # Reset RTIO core to prevent underflows
        self.core.reset()
        self.core.break_realtime() 
        
        #self.cpld.init()
        self.dds.cpld.init()
        
        self.dds.init()

        # switch on dds output
        self.dds.cfg_sw(True)

        # Set attenuation in dB
        self.dds.set_att(1.0 * dB) 
        
        self.dds.set_amplitude(1.0) 


        ## RAM programming
        self.core.break_realtime() 
        self.dds.set_cfr1(ram_enable=0)
        self.dds.cpld.io_update.pulse_mu(8)

        self.dds.cpld.set_profile(0) # Enable the corresponding RAM profile
        
        # Profile 0 is the default
        self.dds.set_profile_ram(
                start = 0, 
                end   = len(self.asf_ram)-1,
                step  = 100, 
                profile = 0, 
                #mode=ad9910.RAM_MODE_CONT_RAMPUP
                mode=ad9910.RAM_MODE_RAMPUP
                )

        self.dds.cpld.io_update.pulse_mu(8)


        # defines the ramp
        self.dds.amplitude_to_ram(self.amp, self.asf_ram)
        self.dds.write_ram(self.asf_ram)
        self.core.break_realtime()
       
        # set frequency
        self.dds.set(
                frequency=2*MHz,
        #        amplitude=1.0,
                profile=0
                )

        # Pass osk_enable=1 to set_cfr1() if it is not an amplitude RAM
        self.dds.set_cfr1(
                ram_enable = 1, 
                ram_destination = ad9910.RAM_DEST_ASF,
                osk_enable = 1
                )
        
        
        self.ttl16.pulse(5*us)

        self.dds.cpld.io_update.pulse_mu(8)
        


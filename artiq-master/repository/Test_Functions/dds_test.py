from artiq.experiment import *

import os
import sys
import time
# from rigol import Rigol_RSA3030
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")


from base_sequences import *


class DDSControl(EnvExperiment):
    
    def build(self):
        # 1. Initialize core device
        self.setattr_device("core")
        
        ## 2. Bind the DDS channel (e.g., AD9910 or AD9914)
        #self.setattr_device("urukul0_ch0")
        #self.setattr_device("urukul0_ch1")
        #self.setattr_device("urukul0_ch2")
        #self.setattr_device("urukul0_ch3")
        #
        #self.setattr_device("urukul1_ch0")
        #self.setattr_device("urukul1_ch1")
        #self.setattr_device("urukul1_ch2")
        #self.setattr_device("urukul1_ch3")

        self.dds  = self.get_device("urukul0_ch0") # Set specific channel
        self.cpld = self.get_device("urukul0_cpld")
        
        #self.setattr_argument('amplitude', NumberValue(default = 0, unit='', min = 0.0, max = 1.0, scale=1,ndecimals=3,step=1))
 
        self.setattr_argument('amplitude_dBm', NumberValue(default = 0.0, unit='', min = -100.0, max = 11.0, scale=1,ndecimals=3,step=1))
       
        self.setattr_argument('frequency', NumberValue(default = 0, unit='MHz', min = 0.0, max = 800.0, scale=1,ndecimals=3,step=1))
        
        self.setattr_argument('attenuation', NumberValue(default = 0, unit='dB', min = 0.0, max = 31.5, scale=1,ndecimals=3,step=1))

        
    @kernel
    def run(self):
        # Reset RTIO core to prevent underflows
        self.core.reset()
        self.core.break_realtime() 
        
        init_dds(self, frequency = self.frequency * MHz, attenuation = self.attenuation * dB, amplitude_dBm = self.amplitude_dBm)

        dds_on(self)
        
        #delay(1000.0*ms)

        #dds_off(self)



        #self.urukul0_ch1.cpld.init()
        #self.urukul0_ch1.init()

        #self.urukul0_ch2.cpld.init()
        #self.urukul0_ch2.init()

        #self.urukul0_ch3.cpld.init()
        #self.urukul0_ch3.init()

        #self.urukul1_ch0.cpld.init()
        #self.urukul1_ch0.init()
 
        #self.urukul1_ch1.cpld.init()
        #self.urukul1_ch1.init()

        #self.urukul1_ch2.cpld.init()
        #self.urukul1_ch2.init()

        #self.urukul1_ch3.cpld.init()
        #self.urukul1_ch3.init()

       
        ## 4. Configure DDS outputs
        ### Set frequency in Hz, phase in cycles (0.0 to 1.0), and attenuation in dB
        #
        ##self.urukul0_ch0.set(frequency = self.frequency * MHz, phase=0.0, amplitude=1.0)
        ##self.urukul0_ch0.set_att(20.0) # Set attenuation in dB
        #
        ##self.urukul1_ch3.set_att(20.0) # Set attenuation in dB
        #
        #self.urukul0_ch0.cfg_sw(False)  # Turn the RF switch ON
        #self.urukul0_ch1.cfg_sw(False)  # Turn the RF switch ON
        #self.urukul0_ch2.cfg_sw(False)  # Turn the RF switch ON
        #self.urukul0_ch3.cfg_sw(False)  # Turn the RF switch ON
        #self.urukul1_ch0.cfg_sw(False)  # Turn the RF switch ON
        #self.urukul1_ch1.cfg_sw(False)  # Turn the RF switch ON
        #self.urukul1_ch2.cfg_sw(False)  # Turn the RF switch ON
        #self.urukul1_ch3.cfg_sw(False)  # Turn the RF switch ON




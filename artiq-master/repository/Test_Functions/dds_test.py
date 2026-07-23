from artiq.experiment import *

class DDSControl(EnvExperiment):
    
    def build(self):
        # 1. Initialize core device
        self.setattr_device("core")
        
        # 2. Bind the DDS channel (e.g., AD9910 or AD9914)
        self.setattr_device("urukul0_ch0")
        self.setattr_device("urukul0_ch1")
        self.setattr_device("urukul0_ch2")
        self.setattr_device("urukul0_ch3")
        
        self.setattr_device("urukul1_ch0")
        self.setattr_device("urukul1_ch1")
        self.setattr_device("urukul1_ch2")
        self.setattr_device("urukul1_ch3")

        self.setattr_argument('frequency', NumberValue(default = 10, unit='MHz', min=1.0, max = 800.0, scale=1,ndecimals=1,step=1))

        
    @kernel
    def run(self):
        # Reset RTIO core to prevent underflows
        self.core.reset()
        self.core.break_realtime() 
        
        # 3. Synchronize with the RTIO timeline
        self.urukul0_ch0.cpld.init()
        self.urukul0_ch0.init()
 
        self.urukul0_ch1.cpld.init()
        self.urukul0_ch1.init()

        self.urukul0_ch2.cpld.init()
        self.urukul0_ch2.init()

        self.urukul0_ch3.cpld.init()
        self.urukul0_ch3.init()

        self.urukul1_ch0.cpld.init()
        self.urukul1_ch0.init()
 
        self.urukul1_ch1.cpld.init()
        self.urukul1_ch1.init()

        self.urukul1_ch2.cpld.init()
        self.urukul1_ch2.init()

        self.urukul1_ch3.cpld.init()
        self.urukul1_ch3.init()

       
        # 4. Configure DDS outputs
        ## Set frequency in Hz, phase in cycles (0.0 to 1.0), and attenuation in dB
        
        #self.urukul0_ch0.set(frequency = self.frequency * MHz, phase=0.0, amplitude=1.0)
        #self.urukul0_ch0.set_att(20.0) # Set attenuation in dB
        
        #self.urukul1_ch3.set_att(20.0) # Set attenuation in dB
        
        self.urukul0_ch0.cfg_sw(False)  # Turn the RF switch ON
        self.urukul0_ch1.cfg_sw(False)  # Turn the RF switch ON
        self.urukul0_ch2.cfg_sw(False)  # Turn the RF switch ON
        self.urukul0_ch3.cfg_sw(False)  # Turn the RF switch ON
        self.urukul1_ch0.cfg_sw(False)  # Turn the RF switch ON
        self.urukul1_ch1.cfg_sw(False)  # Turn the RF switch ON
        self.urukul1_ch2.cfg_sw(False)  # Turn the RF switch ON
        self.urukul1_ch3.cfg_sw(False)  # Turn the RF switch ON




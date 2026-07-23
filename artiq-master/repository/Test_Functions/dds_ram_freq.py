from artiq.experiment import *
from artiq.language.types import TBool, TFloat, TInt32, TInt64, TList, TTuple
from artiq.coredevice import ad9910


import numpy as np



class DDS_RAM(EnvExperiment):
   
    @kernel
    def set_osk_step_size(self, step_size):

        self.dds.write32(ad9910._AD9910_REG_ASF, step_size)

    @kernel
    def set_osk_ramp_rate(self, ramp_rate):

        self.dds.write32(ad9910._AD9910_REG_ASF, ramp_rate << 16)

    @kernel
    def set_osk_asf(self, asf):

        self.dds.set_asf(asf)


    def build(self):
        # 1. Initialize core device
        self.setattr_device("core")
        
        ## 2. Bind the DDS channel (e.g., AD9910 or AD9914)
        #self.setattr_device("urukul0_ch0")

        #self.setattr_argument('frequency', NumberValue(default = 10, unit='MHz', min=1.0, max = 800.0, scale=1,ndecimals=1,step=1))

        self.dds = self.get_device("urukul0_ch0") # Set specific channel
        self.cpld = self.get_device("urukul0_cpld")

        self.setattr_device('ttl16')

        self.f = np.linspace(0.0, 10.0, 4) * MHz
        #self.f = np.linspace(10.0, 11.0, 5) * MHz
        #self.f = np.array([10.0, 10.0, .2, .2, 5.0, 5.0, 10.0, 10.0]) * MHz
        self.f_ram = [0] * len(self.f)

        return

    def get_ramp_array(self):
        return

    @kernel
    def init_dds(self, att = 10.0 * dB, amplitude = 1.0):
        self.dds.cpld.init()
        self.dds.init()

        # Set attenuation in dB
        self.dds.set_att(att * dB) 
        
        self.dds.set_amplitude(amplitude) 

        return


    @kernel
    def prg_freq_ramp(self, 
            step_size = 1*ns,
            profile = 0,
            mode = ad9910.RAM_MODE_RAMPUP
            ):
        
        # RAM programming

        # Switch RAM off
        self.core.break_realtime() 
        self.dds.set_cfr1(ram_enable=0)
        self.dds.cpld.io_update.pulse_mu(8)

        # Set profile
        self.dds.cpld.set_profile(profile) # Enable the corresponding RAM profile
        
        # Profile 0 is the default
        # 250 steps = 1 us
        # 1 step = 4ns
        self.dds.set_profile_ram(
                start = 0, 
                end   = len(self.f_ram)-1,
                step  = int(step_size/4e-9), # in units of 4ns # max = 16-bit = 2^16 - 1 
                profile = profile, 
                mode = mode
                )

        self.dds.cpld.io_update.pulse_mu(8)

        # Convert ramp to machine units and write to RAM
        self.dds.frequency_to_ram(self.f, self.f_ram)
        self.core.break_realtime()
        self.dds.write_ram(self.f_ram)
        self.core.break_realtime()
       
       
        # Pass osk_enable=1 to set_cfr1() if it is not an amplitude RAM
        self.dds.set_cfr1(
                ram_enable = 1, 
                ram_destination = ad9910.RAM_DEST_FTW,
                osk_enable = 1,
                select_auto_osk = 0
                )
 
        # switch on dds output
        self.dds.cfg_sw(True)

        return


    @kernel
    def run(self):
        # Reset RTIO core to prevent underflows
        self.core.reset()
        self.core.break_realtime() 
        

        self.init_dds(att = 6.0 * dB)
        self.prg_freq_ramp(step_size = 15*us)      

        # this starts the ramp at the end of the trigger
        self.ttl16.pulse(5*us)

        self.dds.cpld.io_update.pulse_mu(8)
        


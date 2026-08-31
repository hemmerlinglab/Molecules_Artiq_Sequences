from artiq.experiment import *
from artiq.language.types import TBool, TFloat, TInt32, TInt64, TList, TTuple
from artiq.coredevice import ad9910


import numpy as np



class DDS_RAM_FREQ(EnvExperiment):
   
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
        #self.dds = self.get_device("urukul0_ch1")
        self.cpld = self.get_device("urukul0_cpld")

        self.setattr_device('ttl16')
       
        #self.get_linear_ramp(
        #        start    = 400.0, # in MHz
        #        stop     = 1.0,
        #        duration = 10 * ms)
        
        self.get_linear_ramp(
                start    = 1.0, # in MHz
                stop     = 400.0,
                duration = 10 * ms)


        return

    def get_linear_ramp(self,
            start    = 0.0, # start freq in MHz
            stop     = 1.0, # stop freq in MHz
            duration = 1.0 * ms, # duration of ramp
            min_no   = 1e3 # number of points on the ramp
            ):

        #number_of_points = int(dt / (4*ns))

        number_of_points = int(min_no) # need some reasonable number here

        self.ramp_step_size = duration / number_of_points

        # the actual physical ramping interval
        self.frequency_interval = np.linspace(start, stop, number_of_points) * MHz
        
        # the interval that is programmed into the DDS
        self.frequency_interval_ram = [0] * len(self.frequency_interval)

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
            #mode = ad9910.RAM_MODE_CONT_RAMPUP
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
                end   = len(self.frequency_interval_ram)-1,
                step  = int(step_size/4e-9), # in units of 4ns # max = 16-bit = 2^16 - 1 
                profile = profile, 
                mode = mode
                )

        self.dds.cpld.io_update.pulse_mu(8)

        # Convert ramp to machine units and write to RAM
        self.dds.frequency_to_ram(self.frequency_interval, self.frequency_interval_ram)
        self.core.break_realtime()
        self.dds.write_ram(self.frequency_interval_ram)
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
        
        self.init_dds(att = 0.0 * dB)
        self.prg_freq_ramp(step_size = self.ramp_step_size) 

        # for debugging: this starts the ramp at the end of the trigger to use the scope to trigger the sequence
        self.ttl16.pulse(5*ms)

        self.dds.cpld.io_update.pulse_mu(8)


        #self.dds.cfg_sw(True)
        delay(10*ms)
        self.dds.cfg_sw(False)
        
        self.ttl16.pulse(5*ms)





from artiq.experiment import *
from artiq.coredevice import ad9910

##########################################################################
# DDS functions
##########################################################################

@kernel
def init_dds(self, frequency = 1.0 * MHz, attenuation = 10.0 * dB, amplitude_dBm = 1.0):

    # Convert amplitude in dBm to 0 - 1 scale, see spec sheet of AD9910 with the Urukul giving 11 dBm output power
    amplitude = 10**( (amplitude_dBm - 11.0)/20.0 )

    # this function assumes that one DDS exists and is referenced to as self.dds
    self.core.break_realtime()

    self.dds.cpld.init()
    self.dds.init()

    # Set attenuation in dB
    self.dds.set_att(attenuation) 
   
    # Set amplitude
    self.dds.set_amplitude(amplitude)

    # Set frequency
    self.dds.set(frequency = frequency, phase = 0.0, amplitude = amplitude)

    return

#################################

@kernel
def dds_on(self):
   
    self.core.break_realtime()
    self.dds.cfg_sw(True)

    return

#################################

@kernel
def dds_off(self):
       
    self.core.break_realtime()
    self.dds.cfg_sw(False)

    return

#################################

@kernel
def prg_freq_ramp(
        self, 
        step_size   = 1*ns,
        profile     = 0,
        mode        = ad9910.RAM_MODE_RAMPUP,
        #mode       = ad9910.RAM_MODE_CONT_RAMPUP
        frequency_interval      = [0],
        frequency_interval_ram  = [0]
        ):
   
    #########################
    # RAM programming
    #########################

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
            start   = 0, 
            end     = len(frequency_interval_ram)-1,
            step    = int(step_size/4e-9), # in units of 4ns # max = 16-bit = 2^16 - 1 
            profile = profile, 
            mode    = mode
            )

    self.dds.cpld.io_update.pulse_mu(8)

    # Convert ramp to machine units and write to RAM
    self.dds.frequency_to_ram(frequency_interval, frequency_interval_ram)
    self.core.break_realtime()
    self.dds.write_ram(frequency_interval_ram)
    self.core.break_realtime()
   
    # Pass osk_enable=1 to set_cfr1() if it is not an amplitude RAM
    self.dds.set_cfr1(
            ram_enable      = 1, 
            ram_destination = ad9910.RAM_DEST_FTW, # scans the frequency
            osk_enable      = 1,
            select_auto_osk = 0
            )

    return




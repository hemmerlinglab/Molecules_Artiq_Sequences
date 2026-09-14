from artiq.experiment import *

from base_dds_sequences    import init_dds
from base_zotino_sequences import set_zotino_voltage

##########################################################################
# Core Reset
##########################################################################

@kernel
def reset_core(self):
    self.core.reset()

    return


##########################################################################
# Experiment start
##########################################################################

@kernel
def base_experiment_start(self):

    # debug pulse
    self.ttl8.pulse(10*us)

    self.ttl9.pulse(10*us)

    return


########################################################################
# Relay
########################################################################

@kernel
def relay(self, status):

    self.core.break_realtime()
    
    if status:
        self.ttl13.on()
    else:
        self.ttl13.off()

    return


##########################################################################
# Init sampler
##########################################################################

@kernel
def init_sampler(self):

    self.core.break_realtime()
 
    self.sampler0.init() # initializes sampler device
    
    # Set Channel Gain
    for i in range(8):
        self.sampler0.set_gain_mu(i,0) # (channel,setting) gain is 10^setting

    delay(260*us)

    return


##########################################################################
# Readout sampler
##########################################################################

@kernel
def base_readout_sampler(self):

    delay(self.sampler_delay_time*ms)
    
    smp = [0] * 8 
    for j in range(self.scope_count):
        self.sampler0.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
        
        for k in range(8):
            self.data[k][j] = smp[k]

        delay(self.time_step_size*us) # plus 9us from sample_mu

    return


##########################################################################
# Fire Yag
##########################################################################

@kernel
def base_fire_yag(self):

    if self.yag_on:

        delay(self.yag_fire_time * ms)

        self.ttl4.pulse(15*us) # trigger flash lamp
        delay(140*us) # wait optimal time (for Quantel)
        self.ttl6.pulse(15*us) # trigger q-switch

    return


##########################################################################
# Slowing Pulse
##########################################################################

@kernel
def base_slowing_pulse(self):

    if self.slowing_laser_on:

        delay(self.slowing_laser_start_time * ms)

        # activate the DDS ramp
        self.dds.cpld.io_update.pulse_mu(8)

        # send trigger to BK4053 to switch on AOM
        self.ttl7.pulse(0.1*ms)

        # switch off DDS after delay
        delay( (self.slowing_laser_duration - 0.1) * ms)

        # switch off DDS
        self.dds.cfg_sw(False)

    return


##########################################################################
# Slowing sequence
##########################################################################

@kernel
def fire_and_read(self):

    self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
    
    ###############################
    # Initialization
    ###############################
    
    init_sampler(self)

    ###############################
    # Sequence
    ###############################

    with parallel:

        with sequential:        
            # experiment start 
            base_experiment_start(self)

        with sequential:        
            # fire yag
            base_fire_yag(self)

        with sequential:
            # slowing pulse
            base_slowing_pulse(self)

        with sequential:
            # read out sampler
            base_readout_sampler(self)

    return


##########################################################################

@kernel
def read_rubidium(self):

    self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
    
    ###############################
    # Initialization
    ###############################
    
    init_sampler(self)

    ###############################
    # Sequence
    ###############################

    with parallel:

        with sequential:        
            # experiment start 
            base_experiment_start(self)

        with sequential:
            # read out sampler
            base_readout_sampler(self)

    return



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

@kernel
def fire_and_read(self):

        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        self.sampler0.init()       # initializes sampler device
        
       
        # Set Channel Gain
        for i in range(8):
            self.sampler0.set_gain_mu(i,0) # (channel,setting) gain is 10^setting

        delay(500*us)

        # Data Variable Initialization
        data0 = [0]*self.scope_count # absorption signal data
        data1 = [0]*self.scope_count # fire check data
        data2 = [0]*self.scope_count # uhv data (pmt)
        data3 = [0]*self.scope_count # post select, checks spec blue
        data4 = [0]*self.scope_count # post select, checks slow blue
        data5 = [0]*self.scope_count # absorption signal reference data
        data6 = [0]*self.scope_count # absorption signal reference data
        data7 = [0]*self.scope_count # absorption signal reference data
        
        smp   = [0]*8 # individual sample


    
        ## fire sequence only at a certain time after the pulsetube cycle
        #if self.pulse_tube_sync_wait>0:
        #    delay(self.pulse_tube_sync_wait*ms)
        
        with parallel:

            with sequential:

                # cavity ramp                
                # starting ramp 2ms before yag

                delay((0.01 + self.yag_fire_time + 0.15 + 0.015 + 0.135 + 0.15 + 0.1 - 24.0)*ms) 
                
                self.ttl11.pulse(100*us) # start cavity scan

            with sequential:
                
                # yag sequence

                self.ttl9.pulse(10*us) # experimental start
                

                delay((self.yag_fire_time)*ms) # additional delay since shutter is slow, subtracting delays until yag fires

                delay(150*us)
                self.ttl4.pulse(15*us) # trigger flash lamp
                
                #delay(135*us) # wait optimal time (see Minilite manual)
                delay(140*us) # wait optimal time (for Quantel)
                self.ttl6.pulse(15*us) # trigger q-switch, <--- YAG FIRES ON (60ns after) THIS RISING EDGE
                delay(100*us) # wait until some time after green flash
                
                self.ttl5.pulse(15*us) # trigger uv ccd

            #with sequential:

            #    # uniblitz shutter
            #    
            #    if self.uniblitz_on:
            #        # this is the shutter inside the dewar
            #        # shutter needs 13ms to start opening
            #        delay((self.shutter_start_time)*ms)
            #        self.ttl7.on()
            #        delay((self.shutter_open_time)*ms)
            #        self.ttl7.off()

            with sequential:
                # Slowing laser AOM driver trigger
                if self.slowing_laser_on:
                    # send TTL to trigger BK4053 to switch on Brimrose AOM driver
                    
                    delay((self.slowing_laser_start_time)*ms)
                    self.ttl7.pulse(1*ms)

            with sequential:

                # sampler readout sequence

                delay(self.sampler_delay_time*ms)
                for j in range(self.scope_count):
                    self.sampler0.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
                    data0[j] = smp[0]
                    data1[j] = smp[1]
                    data2[j] = smp[2]
                    data3[j] = smp[3]
                    data4[j] = smp[4]
                    data5[j] = smp[5]
                    data6[j] = smp[6]
                    data7[j] = smp[7]

                    delay(self.time_step_size*us) # plus 9us from sample_mu
        
        ### Allocate and Transmit Data All Channels
        self.set_dataset('ch0', (data0), broadcast = True)
        self.set_dataset('ch1', (data1), broadcast = True)
        self.set_dataset('ch2', (data2), broadcast = True)
        self.set_dataset('ch3', (data3), broadcast = True)
        self.set_dataset('ch4', (data4), broadcast = True)
        self.set_dataset('ch5', (data5), broadcast = True)
        self.set_dataset('ch6', (data6), broadcast = True)
        self.set_dataset('ch7', (data7), broadcast = True)

        return



##########################################################################

@kernel
def no_fire_and_read(self):

        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        self.sampler0.init() # initializes sampler device
        
        # Set Channel Gain
        for i in range(8):
            self.sampler0.set_gain_mu(i,0) # (channel,setting) gain is 10^setting
        #send 5V to relay input(C-NC connects)
        delay(500*us)

        # Data Variable Initialization
        data0 = [0]*self.scope_count # absorption signal data
        data1 = [0]*self.scope_count # fire check data
        data2 = [0]*self.scope_count # uhv data (pmt)
        data3 = [0]*self.scope_count # post select, checks spec blue
        data4 = [0]*self.scope_count # post select, checks slow blue
        data5 = [0]*self.scope_count # absorption signal reference data
        data6 = [0]*self.scope_count # absorption signal reference data
        data7 = [0]*self.scope_count # absorption signal reference data
        
        smp   = [0]*8 # individual sample

        ## fire sequence only at a certain time after the pulsetube cycle
        #if self.pulse_tube_sync_wait>0:
        #    delay(self.pulse_tube_sync_wait*ms)
        
        with parallel:

            with sequential:

                # cavity ramp                
                # starting ramp 2ms before yag

                delay((0.01 + self.yag_fire_time + 0.15 + 0.015 + 0.135 + 0.15 + 0.1 - 24.0)*ms) 
                
                self.ttl11.pulse(100*us) # start cavity scan

            with sequential:
                
                # yag sequence

                self.ttl9.pulse(10*us) # experimental start
                

                delay((self.yag_fire_time)*ms) # additional delay since shutter is slow, subtracting delays until yag fires

                delay(150*us)
                #self.ttl4.pulse(15*us) # trigger flash lamp
                delay(135*us) # wait optimal time (see Minilite manual)
                #self.ttl6.pulse(15*us) # trigger q-switch, <--- YAG FIRES ON (60ns after) THIS RISING EDGE
                delay(100*us) # wait until some time after green flash
                self.ttl5.pulse(15*us) # trigger uv ccd

            with sequential:

                # uniblitz shutter
                
                if self.uniblitz_on:
                    # this is the shutter inside the dewar
                    # shutter needs 13ms to start opening
                    delay((self.shutter_start_time)*ms)
                    self.ttl7.on()
                    delay((self.shutter_open_time)*ms)
                    self.ttl7.off()

            with sequential:

                # sampler readout sequence

                delay(self.sampler_delay_time*ms)
                for j in range(self.scope_count):
                    self.sampler0.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
                    data0[j] = smp[0]
                    data1[j] = smp[1]
                    data2[j] = smp[2]
                    data3[j] = smp[3]
                    data4[j] = smp[4]
                    data5[j] = smp[5]
                    data6[j] = smp[6]
                    data7[j] = smp[7]

                    delay(self.time_step_size*us) # plus 9us from sample_mu
        
        ### Allocate and Transmit Data All Channels
        self.set_dataset('ch0', (data0), broadcast = True)
        self.set_dataset('ch1', (data1), broadcast = True)
        self.set_dataset('ch2', (data2), broadcast = True)
        self.set_dataset('ch3', (data3), broadcast = True)
        self.set_dataset('ch4', (data4), broadcast = True)
        self.set_dataset('ch5', (data5), broadcast = True)
        self.set_dataset('ch6', (data6), broadcast = True)
        self.set_dataset('ch7', (data7), broadcast = True)

        return
########################################################################

@kernel
def relay(self, status):
    self.core.break_realtime()
    if status:
        self.ttl13.on()
    else:
        self.ttl13.off()


##########################################################################

@kernel
def read_rubidium(self):

        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        self.sampler1.init() # initializes sampler device
        # print('made it here')
        ### Set Channel Gain
        for i in range(8):
            self.sampler1.set_gain_mu(i,0) # (channel,setting) gain is 10^setting

        delay(500*us)

        ### Data Variable Initialization
        data0 = [0]*self.scope_count # signal data
        data1 = [0]*self.scope_count # fire check data (Rb absorption data)
        data2 = [0]*self.scope_count # uhv data (pmt)
        data3 = [0]*self.scope_count # post select, checks spec blue
        data4 = [0]*self.scope_count # post select, checks slow blue
        data5 = [0]*self.scope_count # post select, checks slow blue
        data6 = [0]*self.scope_count # post select, checks slow blue
        data7 = [0]*self.scope_count # post select, checks slow blue

        smp = [0]*8 # individual sample

        ### Fire and sample
        with parallel:

            with sequential:
                self.ttl9.pulse(10*us) # experimental start

            with sequential:
                for j in range(self.scope_count):
                    self.sampler1.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
                    data0[j] = smp[0]
                    data1[j] = smp[1]
                    data2[j] = smp[2]
                    data3[j] = smp[3]
                    data4[j] = smp[4]
                    data5[j] = smp[5]
                    data6[j] = smp[6]
                    data7[j] = smp[7]

                    #delay(5*us)
                    delay(self.time_step_size*us) # plus 9us from sample_mu

        # release shutter of slowing laser
        self.ttl8.off()

        ### Allocate and Transmit Data All Channels
        self.set_dataset('ch0', (data0), broadcast = True)
        self.set_dataset('ch1', (data1), broadcast = True)
        self.set_dataset('ch2', (data2), broadcast = True)
        self.set_dataset('ch3', (data3), broadcast = True)
        self.set_dataset('ch4', (data4), broadcast = True)
        self.set_dataset('ch5', (data5), broadcast = True)
        self.set_dataset('ch6', (data6), broadcast = True)
        self.set_dataset('ch7', (data7), broadcast = True)

        return


##########################################################################

@kernel
def init_sampler(self):

    self.core.break_realtime()
 
    self.sampler0.init() # initializes sampler device
    
    # Set Channel Gain
    for i in range(8):
        self.sampler0.set_gain_mu(i,0) # (channel,setting) gain is 10^setting

    delay(260*us)

    ## Data Variable Initialization
    #data0 = [0]*self.scope_count # signal data
    #data1 = [0]*self.scope_count # fire check data
    #data2 = [0]*self.scope_count # uhv data (pmt)
    #data3 = [0]*self.scope_count # post select, checks spec blue
    #data4 = [0]*self.scope_count # post select, checks slow blue
       
    #smp   = [0]*8 # individual sample

    #self.data = [[0]*self.scope_count] * 5 
     
    return


##########################################################################

@kernel
def fire_slow_and_read(self):

    self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
    
    ###############################
    # Initialization
    ###############################
    
    init_sampler(self)

    ###############################
    # Sequence
    ###############################

    with parallel:

        ######################
        # experimental start            
        ######################
        
        with sequential:        


            # debug
            self.ttl8.pulse(10*us)

            self.ttl9.pulse(10*us)
        
        ######################
        # fire yag
        ######################

        with sequential:        
            
            delay(self.yag_fire_time * ms)

            self.ttl4.pulse(15*us) # trigger flash lamp
            delay(140*us) # wait optimal time (for Quantel)
            self.ttl6.pulse(15*us) # trigger q-switch

        ############################
        # activate slowing AOM/EOM
        ############################

        with sequential:

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


        ######################
        # read out sampler
        ######################

        with sequential:
        
            delay(self.sampler_delay_time*ms)
            
            smp = [0] * 8 
            for j in range(self.scope_count):
                self.sampler0.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
                
                for k in range(8):
                    self.data[k][j] = smp[k]

                delay(self.time_step_size*us) # plus 9us from sample_mu


    ###############################################
    # Allocate and Transmit Data All Channels
    ###############################################
    
    self.set_dataset('ch0', (self.data[0]), broadcast = True)
    self.set_dataset('ch1', (self.data[1]), broadcast = True)
    self.set_dataset('ch2', (self.data[2]), broadcast = True)
    self.set_dataset('ch3', (self.data[3]), broadcast = True)
    self.set_dataset('ch4', (self.data[4]), broadcast = True)
    self.set_dataset('ch5', (self.data[5]), broadcast = True)
    self.set_dataset('ch6', (self.data[6]), broadcast = True)
    self.set_dataset('ch7', (self.data[7]), broadcast = True)

    return


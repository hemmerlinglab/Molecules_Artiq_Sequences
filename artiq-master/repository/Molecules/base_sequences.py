from artiq.experiment import *

### Script to run on Artiq
    # Basic Schedule:
    # 1) Trigger YAG Flashlamp
    # 2) Wait 150 us
    # 3) Trigger Q Switch
    # 4) In parallel, read off 2 diodes and PMT
    #
@kernel
def fire_and_read(self):

        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        self.sampler0.init() # initializes sampler device
        # print('made it here')
        ### Set Channel Gain
        for i in range(8):
            self.sampler0.set_gain_mu(i,0) # (channel,setting) gain is 10^setting

        delay(260*us)

        ### Data Variable Initialization
        data0 = [0]*self.scope_count # signal data
        data1 = [0]*self.scope_count # fire check data
        data2 = [0]*self.scope_count # uhv data (pmt)
        data3 = [0]*self.scope_count # post select, checks spec blue
        data4 = [0]*self.scope_count # post select, checks slow blue
        smp = [0]*8 # individual sample

        ## shut slowing laser off before anything starts
        self.ttl8.on()
        delay(25*ms)

        ### Fire and sample
        with parallel:

            with sequential:
                self.ttl9.pulse(10*us) # experimental start

                delay((self.yag_fire_time)*ms) # additional delay since shutter is slow, subtracting delays until yag fires

                delay(150*us)
                self.ttl4.pulse(15*us) # trigger flash lamp
                delay(135*us) # wait optimal time (see Minilite manual)
                self.ttl6.pulse(15*us) # trigger q-switch, <------------------ YAG FIRES ON (60ns after) THIS RISING EDGE
                delay(100*us) # wait until some time after green flash
                self.ttl5.pulse(15*us) # trigger uv ccd

            with sequential:
                if self.uniblitz_on:
                    # this is the shutter inside the dewar
                    # shutter needs 13ms to start opening
                    delay((self.shutter_start_time)*ms)
                    self.ttl7.on()
                    delay((self.shutter_open_time)*ms)
                    self.ttl7.off()

            with sequential:
                delay(self.sampler_delay_time*ms)
                for j in range(self.scope_count):
                    self.sampler0.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
                    data0[j] = smp[0]
                    data1[j] = smp[1]
                    data2[j] = smp[2]
                    data3[j] = smp[3]
                    data4[j] = smp[4]
                    #delay(5*us)
                    delay(self.step_size*us) # plus 9us from sample_mu

        # release shutter of slowing laser
        self.ttl8.off()

        ### Allocate and Transmit Data All Channels
        self.set_dataset('ch0', (data0), broadcast = True)
        self.set_dataset('ch1', (data1), broadcast = True)
        self.set_dataset('ch2', (data2), broadcast = True)
        self.set_dataset('ch3', (data3), broadcast = True)
        self.set_dataset('ch4', (data4), broadcast = True)

        return



@kernel
def read_rubidium(self):

        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        self.sampler1.init() # initializes sampler device
        # print('made it here')
        ### Set Channel Gain
        for i in range(8):
            self.sampler1.set_gain_mu(i,0) # (channel,setting) gain is 10^setting

        delay(260*us)

        ### Data Variable Initialization
        data0 = [0]*self.scope_count # signal data
        data1 = [0]*self.scope_count # fire check data
        data2 = [0]*self.scope_count # uhv data (pmt)
        data3 = [0]*self.scope_count # post select, checks spec blue
        data4 = [0]*self.scope_count # post select, checks slow blue
        smp = [0]*8 # individual sample

        ## shut slowing laser off before anything starts
        self.ttl8.on()
        delay(25*ms)

        ### Fire and sample
        with parallel:

            with sequential:
                self.ttl9.pulse(10*us) # experimental start

            with sequential:
                delay(self.sampler_delay_time*ms)
                for j in range(self.scope_count):
                    self.sampler1.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
                    data0[j] = smp[0]
                    data1[j] = smp[1]
                    data2[j] = smp[2]
                    data3[j] = smp[3]
                    data4[j] = smp[4]
                    #delay(5*us)
                    delay(self.step_size*us) # plus 9us from sample_mu

        # release shutter of slowing laser
        self.ttl8.off()

        ### Allocate and Transmit Data All Channels
        self.set_dataset('ch0', (data0), broadcast = True)
        self.set_dataset('ch1', (data1), broadcast = True)
        self.set_dataset('ch2', (data2), broadcast = True)
        self.set_dataset('ch3', (data3), broadcast = True)
        self.set_dataset('ch4', (data4), broadcast = True)

        return


@kernel
def fire_and_read_slow(self):

        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        self.sampler0.init() # initializes sampler device
        # print('made it here')
        ### Set Channel Gain
        for i in range(8):
            self.sampler0.set_gain_mu(i,0) # (channel,setting) gain is 10^setting

        delay(260*us)

        ### Data Variable Initialization
        data0 = [0]*self.scope_count # signal data
        data1 = [0]*self.scope_count # fire check data
        data2 = [0]*self.scope_count # uhv data (pmt)
        data3 = [0]*self.scope_count # post select, checks spec blue
        data4 = [0]*self.scope_count # post select, checks slow blue
        smp = [0]*8 # individual sample

        ### Fire and sample
        with parallel:

            with sequential:
                self.ttl9.pulse(10*us) # experimental start

                delay((self.yag_fire_time)*ms) # additional delay since shutter is slow, subtracting delays until yag fires

                delay(150*us)
                self.ttl4.pulse(15*us) # trigger flash lamp
                delay(135*us) # wait optimal time (see Minilite manual)
                self.ttl6.pulse(15*us) # trigger q-switch, <------------------ YAG FIRES ON (60ns after) THIS RISING EDGE
                delay(100*us) # wait until some time after green flash
                self.ttl5.pulse(15*us) # trigger uv ccd

            with sequential:
                if self.slowing_laser_shutter_on:
                    # when the trigger is set, the slowing laser is shut off
                    delay((self.slowing_shutter_start_time)*ms)
                    self.ttl8.on()
                    delay((self.slowing_shutter_duration)*ms)
                    self.ttl8.off()


            with sequential:
                if self.uniblitz_on:
                    # this is the shutter inside the dewar
                    # shutter needs 13ms to start opening
                    delay((self.shutter_start_time)*ms)
                    self.ttl7.on()
                    delay((self.shutter_open_time)*ms)
                    self.ttl7.off()

            with sequential:
                delay(self.sampler_delay_time*ms)
                for j in range(self.scope_count):
                    self.sampler0.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
                    data0[j] = smp[0]
                    data1[j] = smp[1]
                    data2[j] = smp[2]
                    data3[j] = smp[3]
                    data4[j] = smp[4]
                    #delay(5*us)
                    delay(self.step_size*us) # plus 9us from sample_mu

        # release shutter of slowing laser
        #self.ttl8.off()

        ### Allocate and Transmit Data All Channels
        self.set_dataset('ch0', (data0), broadcast = True)
        self.set_dataset('ch1', (data1), broadcast = True)
        self.set_dataset('ch2', (data2), broadcast = True)
        self.set_dataset('ch3', (data3), broadcast = True)
        self.set_dataset('ch4', (data4), broadcast = True)

        return


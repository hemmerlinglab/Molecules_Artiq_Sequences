# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime
import os
import time
import csv

import sys
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")

from base_functions import *
from base_sequences import *
from helper_functions import *


# This sequence locks the laser to the wavemeter
# and scans the microwave

# every Experiment needs a build and a run function
class Scan_Diff_Microwave_Alternating(EnvExperiment):

    def build(self):
        base_build(self, which_instruments = ['microwave'])
        self.sequence_filename = os.path.abspath(__file__)

        pulsed_scan_build(self)

        # additional attributes
        my_setattr(self, 'microwave_power', NumberValue(default = -50,unit='dB',scale=1,ndecimals=1,step=1))
        
        return

    def prepare(self):
        # function is run before the experiment, i.e. before run() is called

        self.set_dataset('in_cell_spectrum',     ([0] * self.setpoint_count),broadcast=True)
        self.set_dataset('pmt_spectrum',         ([0] * self.setpoint_count),broadcast=True)

        self.scan_interval = np.linspace(self.setpoint_min, self.setpoint_max, self.setpoint_count)

        my_prepare(self)

        return

    def analyze(self):
        my_analyze(self)

        return

    @kernel
    def reset_core(self):
        self.core.reset()

        return


    def run(self):

        # init flow
        set_helium_flow(self.he_flow, wait_time = self.he_flow_wait)

        # set voltage on plate
        set_zotino_voltage(self, 0, self.plate_voltage)
        
        # set microwave power
        self.microwave.freq(self.scan_interval[0] * 1e6) 
        self.microwave.power(self.microwave_power)
        self.microwave.on()
        
        # init scanning laser
        if self.scanning_laser   == 'Daenerys':
            hlp_frequency_offset = self.offset_laser_Daenerys
        elif self.scanning_laser == 'Hodor':
            hlp_frequency_offset = self.offset_laser_Hodor
        elif self.scanning_laser == 'Davos':
            hlp_frequency_offset = self.offset_laser_Davos

        set_single_laser(self.scanning_laser, hlp_frequency_offset, do_switch = True, wait_time = self.relock_wait_time)

        # pause to wait till laser settles
        time.sleep(1)

        # counter counts setpoints and averages
        counter = 0

        slowing_data = False

        # loop over setpoints
        for n, nu in enumerate(self.scan_interval):

            self.scheduler.pause()

            # scan microwave frequency
            self.current_setpoint = nu * 1.0e6

            self.microwave.freq(self.current_setpoint) 

            for slowing_data in [True, False]:

                # switch on microwave every second data point 
                if not slowing_data:
                    self.microwave.power(self.microwave_power)
                else:
                    self.microwave.power(-100)

                    # reset counter
                    counter -= self.no_of_averages

                print('{0} / {1} setpoints (slowing_shot = {2}, counter = {3})'.format(n+1, self.setpoint_count, slowing_data, counter))

                time.sleep(0.1)


                self.smp_data_avg = {}
                # loop over averages
                for i_avg in range(self.no_of_averages):
                    print(str(i_avg+1) + ' / ' + str(self.no_of_averages) + ' averages')
                    self.scheduler.pause()

                    repeat_shot = True
                    while repeat_shot:
                        # fires yag and reads voltages
                        fire_and_read(self)

                        # readout the data
                        readout_data(self)

                        repeat_shot = check_shot(self)
                        
                        if repeat_shot == False:
                            # upon success add data to dataset
                            average_data(self, i_avg)

                            update_data(self, counter, n, slowing_data = slowing_data)

                            counter += 1

                        time.sleep(self.repetition_time)



            print()
            print()

        # set laser back to initial point
        set_single_laser(self.scanning_laser, hlp_frequency_offset, wait_time = self.lock_wait_time)

        # switch off Helium flow
        set_helium_flow(0.0, wait_time = 0.0)

        # set plate voltage for zero again
        set_zotino_voltage(self, 0, 0)

        # switch off microwave
        self.microwave.off()



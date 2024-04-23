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


# every Experiment needs a build and a run function
class Scan_Single_Laser_Relock(EnvExperiment):

    def build(self):
        base_build(self)
        self.sequence_filename = os.path.abspath(__file__)

        pulsed_scan_build(self)

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

        # init scanning laser
        if self.scanning_laser == 'Daenerys':
            hlp_frequency_offset = self.offset_laser_Daenerys
        elif self.scanning_laser == 'Hodor':
            hlp_frequency_offset = self.offset_laser_Hodor
        elif self.scanning_laser == 'Davos':
            hlp_frequency_offset = self.offset_laser_Davos

        set_single_laser(self.scanning_laser, hlp_frequency_offset + self.scan_interval[0]/1.0e6, do_switch = True, wait_time = self.relock_wait_time)
        set_single_laser('Daenerys', self.offset_laser_Daenerys, do_switch = True, wait_time = self.relock_wait_time)

        # pause to wait till laser settles
        time.sleep(1)

        # counter counts setpoints and averages
        counter = 0
        # loop over setpoints
        for n, nu in enumerate(self.scan_interval):

            self.scheduler.pause()

            self.current_setpoint = hlp_frequency_offset + nu/1.0e6

            # set laser frequencies
            # re-lock lasers
            if n % self.relock_laser_steps == 0:
                print('Relocking laser ..')
                # last laser here should be the one being scanned
                # Needs update when using two lasers
                set_single_laser('Daenerys',          self.offset_laser_Daenerys, do_switch = True, wait_time = self.relock_wait_time)
                set_single_laser(self.scanning_laser, self.current_setpoint,      do_switch = True, wait_time = self.relock_wait_time)
            else:
                set_single_laser(self.scanning_laser, self.current_setpoint, do_switch = True, wait_time = self.relock_wait_time)

            ## fire scanning cavity calibration shots
            #print('Fire calibration shots')
            #for k_dummy in range(3):
            #    print(k_dummy)
            #    fire_dummy_shot(self)
            #    time.sleep(1.0)


            print(str(n+1) + ' / ' + str(self.setpoint_count) + ' setpoints')

            if n == 0:
                time.sleep(0.1)
            else:
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

                        update_data(self, counter, n)

                        counter += 1

                    time.sleep(self.repetition_time)

            print()
            print()

        # set laser back to initial point
        set_single_laser(self.scanning_laser, hlp_frequency_offset + self.scan_interval[0]/1.0e6, wait_time = self.lock_wait_time)
        # switch off Helium flow
        set_helium_flow(0.0, wait_time = 0.0)



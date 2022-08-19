# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime
import os
import time
import csv

from base_functions_parameter_scan import *
from base_sequences import *

import sys
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")

from helper_functions import *


# every Experiment needs a build and a run function
class Scan_Parameter(EnvExperiment):
    
    def build(self):
        base_build(self)
 
    def prepare(self):
        # function is run before the experiment, i.e. before run() is called
        my_prepare(self)

    def analyze(self):
        my_analyze(self)

    @kernel
    def reset_core(self):
        self.core.reset()


    def set_flow(self, flow, wait_time = 10.0):

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('192.168.42.30', 63800)
        print('connecting to %s port %s' % server_address)
        sock.connect(server_address)
    
        message = "{0:2.1f}".format(flow / 5.0)
        sock.sendall(message.encode())
        sock.close()
 
        time.sleep(wait_time)

        return


    def run(self):

        # counter counts setpoints and averages
        counter = 0
        # loop over setpoints
        for n, flow in enumerate(self.scan_interval): 

            # set Helium flow
            self.set_flow(flow)
            self.current_setpoint = flow

            print(str(n+1) + ' / ' + str(self.setpoint_count) + ' setpoints')

            self.smp_data_avg = {}
            # loop over averages
            for i_avg in range(self.scan_count):                
                print(str(i_avg+1) + ' / ' + str(self.scan_count) + ' averages')
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
                        average_data(self, first_avg = (i_avg == 0))
                        
                        if i_avg == 0:
                            self.ch0_avg = self.smp_data[self.smp_data_sets['ch0']]
                            self.ch2_avg = self.smp_data[self.smp_data_sets['ch2']]
                        else:
                            self.ch0_avg = (self.ch0_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch0']]) / (i_avg+1.0)
                            self.ch2_avg = (self.ch2_avg * (i_avg) + self.smp_data[self.smp_data_sets['ch2']]) / (i_avg+1.0)

                        update_data(self, counter, n)

                        counter += 1
                    
                    time.sleep(self.repetition_time)

            print()
            print()

        self.set_flow(0.0)

# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime
import os
import time
import csv
import socket

from base_functions import *
from base_sequences import *

import sys
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/Drivers")

from helper_functions import *


# every Experiment needs a build and a run function
class Raster_Target_New(EnvExperiment):
    def build(self):
                
        base_build(self)
        
        # x
        my_setattr(self, 'min_x',NumberValue(default=3.5,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'max_x',NumberValue(default=4.6,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'steps_x',NumberValue(default=3,unit='',scale=1,ndecimals=0,step=1))
        
        # y
        my_setattr(self, 'min_y',NumberValue(default=3.25,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'max_y',NumberValue(default=5.50,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'steps_y',NumberValue(default=3,unit='',scale=1,ndecimals=0,step=1))

    def prepare(self):
        # function is run before the experiment, i.e. before run() is called
        my_prepare(self)

    def analyze(self):
        my_analyze(self)

    @kernel
    def reset_core(self):
        self.core.reset()


    def run(self):

        # init lasers
        set_lasers(self, init = True)
        
        counter = 0
        # loop over setpoints
        for nx, xpos in enumerate(self.scan_x_interval): 
           for ny, ypos in enumerate(self.scan_y_interval): 

                print("{0}/{1}".format(counter,self.scan_count*len(self.scan_x_interval)*len(self.scan_y_interval)))

                print('Setting x/y position to ' + str(xpos) + '/' + str(ypos))

                # move mirrors
                # init connection to python server to send commands to move mirrors
                # Create a TCP/IP socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = ('192.168.42.20', 62000)
                print('connecting to %s port %s' % server_address)
                sock.connect(server_address)

                message = "{0:5.3f}/{1:5.3f}".format(xpos, ypos)
                print('Moving mirrors ... ' + message)
                
                #print('Sending message ...')
                sock.sendall(message.encode())                
                #print('Done sending ...')
               
                # allow for some time at the edges
                if (nx == 0) or (ny == 0):
                    print('Sleeping for 1 ...')
                    time.sleep(1)

                sock.close()
                print('Socket closed ...')


                hlp_counter = counter
                # reset counter to accommodate for the slow on/slow off sequence
                counter = hlp_counter
    
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
        
                        repeat_shot = self.check_shot()
                        if repeat_shot == False:                        
                            # upon success add data to dataset
                            average_data(self, first_avg = (i_avg == 0))
                            
                            update_data(self, counter, nx, ny)
        
                            counter += 1
                        
                        time.sleep(self.repetition_time)

                print()
                print()


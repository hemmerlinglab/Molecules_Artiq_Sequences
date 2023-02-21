# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime
import os
import time
import csv
import socket

import sys
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")

from base_functions import *
from base_sequences import *
from helper_functions import *


# every Experiment needs a build and a run function
class Raster_Target(EnvExperiment):
    def build(self):                
        base_build(self)
        self.sequence_filename = os.path.abspath(__file__)
        
        pulsed_scan_build(self)

        # x
        my_setattr(self, 'min_x',NumberValue(default=3.5,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'max_x',NumberValue(default=4.6,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'steps_x',NumberValue(default=3,unit='',scale=1,ndecimals=0,step=1))
        
        # y
        my_setattr(self, 'min_y',NumberValue(default=3.25,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'max_y',NumberValue(default=5.50,unit='',scale=1,ndecimals=3,step=0.001))
        my_setattr(self, 'steps_y',NumberValue(default=3,unit='',scale=1,ndecimals=0,step=1))
        return

    def prepare(self):
        # function is run before the experiment, i.e. before run() is called

        self.scan_x_interval = np.linspace(self.min_x, self.max_x, self.steps_x)
        self.scan_y_interval = np.linspace(self.min_y, self.max_y, self.steps_y)

        self.setpoint_count = len(self.scan_x_interval) * len(self.scan_y_interval)

        self.scan_interval = [0] # dummy

        target_img_incell = [[0] * len(self.scan_y_interval)] * len(self.scan_x_interval) 
        self.set_dataset('target_img_incell',(np.array(target_img_incell)),broadcast=True)

        (mesh_X, mesh_Y) = np.meshgrid(self.scan_x_interval, self.scan_y_interval)
        mesh_X = mesh_X.flatten()
        mesh_Y = mesh_Y.flatten()

        self.set_dataset('posx',      (mesh_X),broadcast=True)
        self.set_dataset('posy',      (mesh_Y),broadcast=True)


        self.smp_data_sets = {
            'ch0' : 'absorption',
            'ch1' : 'fire_check',
            'ch2' : 'pmt',
            'ch3' : 'slow_check',
            'ch4' : 'spec_check'
            }

        data_to_save = [{'var' : 'set_points', 'name' : 'set_points'},
                             {'var' : 'posx', 'name' : 'posx'},
                             {'var' : 'posy', 'name' : 'posy'},
                             {'var' : 'times', 'name' : 'times'},
                             {'var' : 'ch0_arr', 'name' : self.smp_data_sets['ch0']},
                             {'var' : 'ch1_arr', 'name' : self.smp_data_sets['ch1']},
                             {'var' : 'ch2_arr', 'name' : self.smp_data_sets['ch2']},
                             {'var' : 'ch3_arr', 'name' : self.smp_data_sets['ch3']},
                             {'var' : 'ch4_arr', 'name' : self.smp_data_sets['ch4']},
                             {'var' : 'target_img_incell', 'name' : 'img'},
                             ]


        my_prepare(self, data_to_save = data_to_save)
 
       
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

        # init lasers
        set_single_laser('Davos', self.offset_laser_Davos, do_switch = True, wait_time = self.relock_wait_time)
        
        counter = 0
        # loop over setpoints
        for nx, xpos in enumerate(self.scan_x_interval): 
           for ny, ypos in enumerate(self.scan_y_interval): 

                print("{0}/{1}".format(counter,self.no_of_averages*len(self.scan_x_interval)*len(self.scan_y_interval)))
            
                self.current_setpoint = 0.0

                # move mirror

                # allow for some time at the edges
                if (nx == 0) or (ny == 0):
                    move_yag_mirror(xpos, ypos, wait_time = 1)
                else:
                    move_yag_mirror(xpos, ypos)
                

                hlp_counter = counter
                # reset counter to accommodate for the slow on/slow off sequence
                counter = hlp_counter
    
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
                            
                            update_data_raster(self, counter, nx, ny)
        
                            counter += 1
                        
                        time.sleep(self.repetition_time)

                print()
                print()

        # switch off Helium flow
        set_helium_flow(0.0, wait_time = 0.0)



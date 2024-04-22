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
from scan_functions import scan_parameter


class General_Scan(EnvExperiment):
    
    ##############################################################

    def build(self):

        base_build(self)
        self.sequence_filename = os.path.abspath(__file__)

        pulsed_scan_build(self)

        return

    
    ##############################################################
    
    def prepare(self):

        my_prepare(self)

    
    ##############################################################
    
    def analyze(self):

        my_analyze(self)
    
        return

    
    ##############################################################

    def run(self):

        if self.scan_ok:

            for my_ind in range(len(self.scan_values)):

                self.scheduler.pause()

                # set the new parameter
                scan_parameter(self, my_ind)



    return





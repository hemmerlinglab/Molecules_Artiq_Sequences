from artiq.experiment import *

import os
import sys
import time
# from rigol import Rigol_RSA3030
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")

import numpy as np

from base_sequences import *

class Reset_All_DDS(EnvExperiment):
    
    def build(self):
        # 1. Initialize core device
        self.setattr_device("core")
        
        ## 2. Bind the DDS channel (e.g., AD9910 or AD9914)
        
        self.dds0 = []
        self.dds1 = []
        for k in range(4):
            self.dds0.append(self.get_device("urukul0_ch{0}".format(k)))
            self.dds1.append(self.get_device("urukul1_ch{0}".format(k)))
        
        return

    @kernel
    def do_run(self, dds):
        # Reset RTIO core to prevent underflows
        self.core.reset()
        self.core.break_realtime() 

        dds.cpld.init()
        dds.init()
        dds.cfg_sw(False)

        return

    def run(self):

        for k in self.dds0:
            print(k)
            self.do_run(k)

        for k in self.dds1:
            print(k)
            self.do_run(k)

        return



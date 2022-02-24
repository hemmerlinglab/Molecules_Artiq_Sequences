import sys
import os
import select
from artiq.experiment import *
from artiq.coredevice.ad9910 import AD9910
from artiq.coredevice.ad53xx import AD53xx
import time
import numpy as np

def print_underflow():
    print('RTIO underflow occured')

class DAQ5(EnvExperiment):
    def build(self):
        self.setattr_device('core')
        # define ttl port being used for pmt test
        self.setattr_device('ttl3') # experiment start#
#    @kernel
@kernel
def run_pmt(self):
    self.core.break_realtime()
    while not self.scheduler.check_pause():
        self.core.break_realtime() #sets "now" to be in the near future (in artiq manual)
        t_count = self.ttl3.gate_rising(self.duration*ms)
        pmt_count = self.ttl3.count(t_count)
        self.append("pmt_counts", pmt_count)
        self.append("pmt_counts_866_off", -1)




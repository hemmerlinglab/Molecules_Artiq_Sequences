from artiq.experiment import *

import os
import sys
import time
import numpy as np

sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server")

from base_sequences import *
from my_prepare_functions import get_basefilename, save_config
from my_build_functions import my_setattr
from my_instrument_functions  import move_yag_mirror, prepare_dds_ramp, set_single_laser, prepare_bk4053, program_siglent_ramp

from SDG_6052X           import SDG_6052X
from rigol      import Rigol_RSA3030

class AWG_Test(EnvExperiment):
    
    def build(self):

        self.config_dict    = []
        self.config_dict_no = {}
        
        self.sequence_filename = os.path.abspath(__file__)
        self.config_dict.append({'par' : 'sequence_file', 'val' : self.sequence_filename, 'cmt' : 'Filename of the main sequence file'})

        self.setattr_device("core")
       
        self.dds  = self.get_device("urukul0_ch0") # Set specific channel
        self.cpld = self.get_device("urukul0_cpld")
       
        # define attributes
        my_setattr(self,'amplitude_dBm', NumberValue(default = 0.0, unit='', min = -100.0, max = 11.0, scale=1,ndecimals=3,step=1))
        my_setattr(self,'frequency', NumberValue(default = 10, unit='MHz', min = 0.0, max = 800.0, scale=1,ndecimals=3,step=1))
        my_setattr(self,'attenuation', NumberValue(default = 0, unit='dB', min = 0.0, max = 31.5, scale=1,ndecimals=3,step=1))
        my_setattr(self,'dds_on', BooleanValue(default=False))
        my_setattr(self,'dc_offset', NumberValue(default = 0, unit='V', min = 0.0, max = 1.0, scale=1,ndecimals=3,step=1))
      
        self.setattr_device('ttl7') # slowing shutter
        self.setattr_device('ttl8') # slowing shutter
        self.setattr_device('ttl9') # experimental start
        self.setattr_device('ttl10') # experimental start
        
        self.setattr_device('ttl15') # experimental start


        # define instruments
        self.spectrum_analyzer      = Rigol_RSA3030()

        #self.bk4053                 = BK4053()
            
        self.spec_result = []

        self.awg = SDG_6052X()   

        return


    @kernel
    def my_run(self):
    
        self.core.reset()
        
        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        
        # send triggers to pulse AOM and EOM
        with parallel:
        
            with sequential:
                
                # send trigger to Siglent to switch on EOM ramp
                
                self.ttl8.pulse(1*ms)

            with sequential:
                
                # send trigger to trigger scope
                self.ttl15.pulse(1*ms)
 
            with sequential:
                # send trigger to RF Switch
                self.ttl10.pulse(self.slowing_laser_duration * ms)
    
        
        return


    def run(self):

        print('Scan start ...')

        channel = 2
        
        
        self.awg.send(f'C{channel}:BTWV STATE,ON')  # Turn burst mode ON
        #print(self.awg.query(f'C{channel}:BTWV?'))  # Turn burst mode ON


        Omega_b_start = 500.0
        Omega_a_stop = 10.0
        
        self.spectrum_analyzer.set_freq([(Omega_a_stop - 2.0) * 1e6, (Omega_b_start + 2.0) * 1e6])

        #Omega_b_start = 100
        #Omega_a_stop = 10

        #Omega_b_start = 3*1e-6
        #Omega_a_stop = 3*1e-6

        self.slowing_laser_duration = 3.0
                    
        program_siglent_ramp(self,
                    channel = channel,
                    start_freq = Omega_b_start, 
                    stop_freq = Omega_a_stop, 
                    duration = self.slowing_laser_duration * ms
                    )
        
        self.awg.on(channel = channel)
        self.awg.send(f'C{channel}:BTWV STATE,ON')  # Turn burst mode ON
        
        for k in range(2):

            print(k)

            self.my_run()

            time.sleep(0.5)

        print('Done.')

        #for k in self.scan_interval:
       
        #    print('Scan point {0}'.format(k))
        #
        #    #k_val = 10**( (k - 11.0)/20.0 )
        #    k_val = k

        #    self.base_run(k_val)

        #    time.sleep(2)

        #    hlp = self.spectrum_analyzer.get_trace()
        #    
        #    self.spec_result.append(hlp[:, 0])
        #    self.spec_result.append(hlp[:, 1])
        
        self.awg.off(channel = channel)


        return



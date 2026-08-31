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

from rigol      import Rigol_RSA3030
from bk_4053    import BK4053

class DDS_Double_Scan(EnvExperiment):
    
    def build(self):

        self.config_dict    = []
        self.config_dict_no = {}
        
        self.sequence_filename = os.path.abspath(__file__)
        self.config_dict.append({'par' : 'sequence_file', 'val' : self.sequence_filename, 'cmt' : 'Filename of the main sequence file'})

        self.setattr_device("core")
       
        self.dds0  = self.get_device("urukul0_ch2") # Set specific channel
        self.dds1  = self.get_device("urukul0_ch3") # Set specific channel
        self.dds2  = self.get_device("urukul0_ch1") # Set specific channel
       
        # define attributes
        my_setattr(self,'amplitude_dBm', NumberValue(default = 0.0, unit='', min = -100.0, max = 11.0, scale=1,ndecimals=3,step=1))
        my_setattr(self,'frequency', NumberValue(default = 10, unit='MHz', min = 0.0, max = 800.0, scale=1,ndecimals=3,step=1))
        my_setattr(self,'attenuation', NumberValue(default = 0, unit='dB', min = 0.0, max = 31.5, scale=1,ndecimals=3,step=1))
        my_setattr(self,'dds_on', BooleanValue(default=False))
        my_setattr(self,'dc_offset', NumberValue(default = 0, unit='V', min = 0.0, max = 1.0, scale=1,ndecimals=3,step=1))
       
        # define instruments
        self.spectrum_analyzer      = Rigol_RSA3030()

        self.bk4053                 = BK4053()
            
        self.spec_result = []

        return

    @kernel
    def base_run(self, new_val):
        # Reset RTIO core to prevent underflows
        self.core.reset()
        self.core.break_realtime() 
        
        # Convert amplitude in dBm to 0 - 1 scale, see spec sheet of AD9910 with the Urukul giving 11 dBm output power
        amplitude = 10**( (self.amplitude_dBm - 11.0)/20.0 )

        # this function assumes that one DDS exists and is referenced to as self.dds

        self.dds0.cpld.init()
        self.dds0.init()

        self.dds1.cpld.init()
        self.dds1.init()

        self.dds2.cpld.init()
        self.dds2.init()


        # Set attenuation in dB
        self.dds0.set_att(self.attenuation) 
        self.dds1.set_att(self.attenuation) 
        self.dds2.set_att(self.attenuation) 
       
        # Set frequency
        self.dds0.set(frequency = new_val * MHz, phase = 0.0, amplitude = amplitude)
        self.dds1.set(frequency = 400.0 * MHz, phase = 0.0, amplitude = amplitude)
        self.dds2.set(frequency = 400.0 * MHz, phase = 0.0, amplitude = amplitude)

        self.dds0.cfg_sw(True)
        self.dds1.cfg_sw(True)
        self.dds2.cfg_sw(True)

        return

    @kernel
    def end_run(self):
        
        self.core.break_realtime() 
        
        self.dds0.cfg_sw(False)
        self.dds1.cfg_sw(False)
        self.dds2.cfg_sw(False)

        return


    def run(self):

        print('Scan start ...')

        self.spectrum_analyzer.set_freq([1e6, 905e6])

        self.bk4053.set_dc_output(1, self.dc_offset)
        self.bk4053.on(1)
        
        self.scan_interval = np.linspace(5, 400, 25)
        
        #self.scan_interval = np.linspace(-40, 11, 50)
        
        for k in self.scan_interval:
       
            print('Scan point {0}'.format(k))
        
            #k_val = 10**( (k - 11.0)/20.0 )
            k_val = k

            self.base_run(k_val)

            time.sleep(2)

            hlp = self.spectrum_analyzer.get_trace()
            
            self.spec_result.append(hlp[:, 0])
            self.spec_result.append(hlp[:, 1])

        self.end_run()

        return

    def analyze(self):
 
        # get basefilename
        get_basefilename(self)

        print()
        print('Saving data ... {0}'.format(self.scan_timestamp))
        # Write data to files
                
        for var in ['scan_interval', 'spec_result']:

            arr = eval('self.{0}'.format(var))

            f_hlp = open("{0}_{1}".format(self.basefilename, var),'w')
            np.savetxt(f_hlp, arr, delimiter=",")
            f_hlp.close()

    
        save_config(self.basefilename, self.config_dict)
        
        print()
        print('Scan done.')

 

        return




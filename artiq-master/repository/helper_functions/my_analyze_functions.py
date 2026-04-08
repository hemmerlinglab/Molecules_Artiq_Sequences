from artiq.experiment import *

import os
import sys
import numpy as np

sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server/Quantel_Yag")

from scan_functions          import reset_scan_parameter
from my_instrument_functions import reset_instruments, close_instruments
from my_prepare_functions    import save_config
from base_sequences          import relay
from quantel                 import Quantel_Yag

#######################################################################################################

def my_analyze(self):

    # reset scan value to setting in parameter
    reset_scan_parameter(self)

    # function is run after the experiment, i.e. after run() is called
    print('Saving data ...')
    save_all_data(self)

    # overwrite config file with complete configuration
    self.config_dict.append({'par' : 'Status', 'val' : True, 'cmt' : 'Run finished.'})
    save_config(self.basefilename, self.config_dict)

    # add scan to scan_list
    add_scan_to_list(self)

    # save Yag status
    save_yag_status(self)

    # finish scan
    print('Scan ' + self.basefilename + ' finished.')
    print('Scan finished.')
    relay(self, status = False)

    ####################################
    # Switch off instruments
    ####################################

    reset_instruments(self)

    ####################################
    # Close instruments
    ####################################

    close_instruments(self)



    # Play sound that scan is finished
    os.system('mpg321 -quiet ~/boat.mp3')
    
    
    return


#######################################################################################################

def save_all_data(self):
    
    # loops over data_to_save and saves all data sets in the array self.data_to_save
    for hlp in self.data_to_save:
        # transform into numpy arrays
        arr = np.array(self.get_dataset(hlp['var']))
       
        if hlp['var'] == "transfer_lock_traces":

            arr = arr.reshape(arr.shape[1] * arr.shape[0], arr.shape[2])
        
        if hlp['var'] == "transfer_lock_times":
            
            # save only one time trace

            arr = arr[0]

        if (len(arr.shape) == 3) and (arr.shape[2] == 2):

            # needs to flatten 3D array
            # arr     = [ [[x1, x2], [y1, y2]], [[x3, x4], [y3, y4], ...]
            # new_arr = [ [x1, x2], [y1, y2], [x3, x4], [y1, y2], ...]

            #print(arr.shape)

            xarr = arr[:, :, 0]
            yarr = arr[:, :, 1]

            hlp_arr = []
            for k in range(arr.shape[0]):

                hlp_arr.append(xarr[k])
                hlp_arr.append(yarr[k])

            arr = np.array(hlp_arr)

        # Write Data to Files
        f_hlp = open(self.basefilename + '_' + hlp['var'],'w')
        np.savetxt(f_hlp, arr, delimiter=",")
        f_hlp.close()

    return


#######################################################################################################

def add_scan_to_list(self):
    
    # Write Data to Files
    f_hlp = open(self.datafolder + '/' + self.today + '/' + 'scan_list_' + self.today, 'a')
    f_hlp.write(self.scan_timestamp + '\n')
    f_hlp.close()

    return


#######################################################################################################

def save_yag_status(self):
        
    path = '/home/molecules/software/Molecules_Artiq_Sequences/python_server/Quantel_Yag/quantel.py' 

    os.system('python {0} {1}'.format(path, self.basefilename + '_yag_status'))

    #yag = Quantel_Yag()

    #yag.log(self.basefilename + '_yag_status')

    #yag.close()

    return
 


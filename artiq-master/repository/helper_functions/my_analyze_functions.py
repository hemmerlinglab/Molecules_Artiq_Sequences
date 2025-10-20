from artiq.experiment import *

import os
import numpy as np

from scan_functions          import reset_scan_parameter
from my_instrument_functions import reset_instruments, close_instruments
from my_prepare_functions    import save_config


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

    add_scan_to_list(self)

    print('Scan ' + self.basefilename + ' finished.')
    print('Scan finished.')

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
       
        if hlp['var'] == "transfer_lock_trace":

            arr = arr.reshape(arr.shape[1] * arr.shape[0], arr.shape[2])

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
        



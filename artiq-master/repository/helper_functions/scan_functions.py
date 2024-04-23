import time
import numpy as np

from base_sequences   import set_mesh_voltage, set_multipoles, set_loading_pulse, set_extraction_pulse, set_MCP_voltages, update_detection_time



# List of scannable parameters

SCANNABLE_PARAMETERS = 
        ['microwave_power',
         'microwave_frequency',
        ]



########################################################################

def scan_parameter(self, my_ind, scan_check = False, reset_value = False):

    # This function allows for scanning any parameter
    # In prepare, it checks whether the scanning function _scan_<parameter> exists and whether the parameter is in range

    ###############################################
    # Get the new setpoint for the parameter
    ###############################################

    if not reset_value:
        val = self.scan_values[my_ind]
    else:
        # reset the value to the one in the parameter listing
        print('Resetting scanning parameter ...')
        val = eval('self.' + self.scanning_parameter)


    ###############################################
    # Output the scan point
    ###############################################

    if not scan_check and not reset_value:
        print("Scanning parameter {3}: {2} ({0}/{1})".format(my_ind, len(self.scan_values), val, self.scanning_parameter))


    ###############################################
    # Change the parameter to the new value
    ###############################################

    if self.scanning_parameter in SCANNABLE_PARAMETERS:

        return eval('_scan_' + self.scanning_parameter + '(self, val, self.scan_values, scan_check = scan_check)')

    else:
        
        print('Parameter to scan {0} has no scanning function yet'.format(self.scanning_parameter))        
        return 0

    return


########################################################################

def limit_check(par, scan_values, limits):
    
    check = (np.min(scan_values) >= limits[0]) and (np.max(scan_values) <= limits[1])

    if not check:
        print('Scan range out of bounds for parameter {0}.'.format(par))

    return check


########################################################################

def _scan_microwave_power(self, val, scan_values, scan_check = False):

    if scan_check:

        # check if the scan range is within the limits

        return limit_check(self.scanning_parameter, scan_values, [-100.0, 10.0])
    
    else:

        # add specific code for parameter change here, including any necessary wait times

        self.microwave.power(val)

        return 1

    return






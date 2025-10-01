import time
import numpy as np

from my_instrument_functions import set_single_laser, set_helium_flow, set_cavity_ramp_sp

########################################################################

def get_scannable_parameters():

    # List of scannable parameters
    
    SCANNABLE_PARAMETERS = [
             'microwave_power',
             'microwave_frequency',
             'offset_laser_Daenerys',
             'he_flow',
             'repetition_time',
             'offset_laser_Hodor',
             'offset_laser_Davos',
             'cavity_ramp'
            ]

    return SCANNABLE_PARAMETERS


########################################################################

def scan_parameter(self, my_ind, scan_check = False, reset_value = False):

    # This function allows for scanning any parameter
    # In prepare, it checks whether the scanning function _scan_<parameter> exists and whether the parameter is in range

    ###############################################
    # Get the new setpoint for the parameter
    ###############################################

    if not reset_value:
        val = self.scan_values[my_ind]        
        self.current_setpoint = val
    else:
        # reset the value to the one in the parameter listing
        print('Resetting scanning parameter ...')
        if not self.scanning_parameter == 'dummy' and not self.scanning_parameter == 'cavity_ramp':
            val = eval('self.' + self.scanning_parameter)
        elif self.scanning_parameter == 'cavity_ramp':
            eval('_scan_cavity_ramp(self, 0, self.scan_values, scan_check = scan_check)')
            val = 0.0
        else:
            val = 0.0


    ###############################################
    # Output the scan point
    ###############################################

    if not scan_check and not reset_value:
        print("Scanning {3}: ({0:2.0f}/{1}) - value: {2:10.2f}".format(my_ind + 1, len(self.scan_values), val, self.scanning_parameter))

    ###############################################
    # Change the parameter to the new value
    ###############################################

    if (self.scanning_parameter in get_scannable_parameters()) or (self.scanning_parameter == 'dummy'):

        return eval('_scan_' + self.scanning_parameter + '(self, val, self.scan_values, scan_check = scan_check)')

    else:
        
        print('Parameter to scan {0} has no scanning function yet'.format(self.scanning_parameter))        
        return 0

    return


#######################################################################################################

def reset_scan_parameter(self):
    
    # sets the value of the scanned parameter to the one in the parameter listing

    scan_parameter(self, 0, reset_value = True)

    return


########################################################################

def limit_check(par, scan_values, limits):
    
    check = (np.min(scan_values) >= limits[0]) and (np.max(scan_values) <= limits[1])

    if not check:
        print()
        print('Scan range out of bounds for parameter {0}.'.format(par))
        print()

    return check


########################################################################

def _scan_dummy(self, val, scan_values, scan_check = False):

    if scan_check:

        # check if the scan range is within the limits

        return 1
    
    else:

        # add specific code for parameter change here, including any necessary wait times        

        return 1

    return


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


########################################################################

def _scan_microwave_frequency(self, val, scan_values, scan_check = False):

    if scan_check:

        # check if the scan range is within the limits

        return limit_check(self.scanning_parameter, scan_values, [15.0, 20.0e3]) # 15 MHz to 20 GHz
    
    else:

        # add specific code for parameter change here, including any necessary wait times

        self.microwave.freq(val * 1e6)

        return 1

    return


###############################################################################

def _scan_he_flow(self, val, scan_values, scan_check = False):

    if scan_check:

        # check if the scan range is within the limits

        return limit_check(self.scanning_parameter, scan_values, [0, 25]) # 0 sccm to 20 sccm
    
    else:

        # add specific code for parameter change here, including any necessary wait times
        set_helium_flow(val, wait_time = self.he_flow_wait)

        return

    return


########################################################################

def _scan_repetition_time(self, val, scan_values, scan_check = False):

    if scan_check:

        # check if the scan range is within the limits

        return limit_check(self.scanning_parameter, scan_values, [0.1, 100.0])
    
    else:

        # add specific code for parameter change here, including any necessary wait times

        self.repetition_time = val

        return 1

    return




########################################################################
# Laser Scan Functions
########################################################################

def _scan_offset_laser_Hodor(self, val, scan_values, scan_check = False):

    if scan_check:

        # check if the scan range is within the limits

        return limit_check(self.scanning_parameter, scan_values, [-10.0e3, 10.0e3]) # in MHz
    
    else:

        # add specific code for parameter change here, including any necessary wait times
        
        frequency = self.offset_laser_Hodor + val/1.0e6

        set_single_laser('Hodor', frequency, do_switch = True, wait_time = self.relock_wait_time)

        return 1

    return


########################################################################

def _scan_offset_laser_Daenerys(self, val, scan_values, scan_check = False):

    if scan_check:

        # check if the scan range is within the limits

        return limit_check(self.scanning_parameter, scan_values, [-10.0e3, 10.0e3]) # in MHz
    
    else:

        # add specific code for parameter change here, including any necessary wait times
        
        frequency = self.offset_laser_Daenerys + val/1.0e6

        set_single_laser('Daenerys', frequency, do_switch = True, wait_time = self.relock_wait_time)

        return 1

    return


######################################################################################################

def _scan_offset_laser_Davos(self, val, scan_values, scan_check = False):

    if scan_check:

        # check if the scan range is within the limits

        return limit_check(self.scanning_parameter, scan_values, [-10.0e3, 10.0e3]) # in MHz
    
    else:

        # add specific code for parameter change here, including any necessary wait times
        
        frequency = self.offset_laser_Davos + val/1.0e6

        set_single_laser('Davos', frequency, do_switch = True, wait_time = self.relock_wait_time)

        return 1

    return


######################################################################################################

def _scan_cavity_ramp(self, val, scan_values, scan_check = False):

    if scan_check:

        # check if the scan range is within the limits

        return limit_check(self.scanning_parameter, scan_values, [-500.0, 500.0]) # in MHz
    
    else:

        # add specific code for parameter change here, including any necessary wait times
        
        set_cavity_ramp_sp(val)

        return 1

    return






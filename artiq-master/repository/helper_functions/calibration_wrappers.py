import numpy as np

from atom_lines import get_transition_freq

#####################################################################

def get_Rb85_calibration_transitions(add_crossover_transitions = True):

    atom = 'Rb85'

    Ji = 'S1/2'
    Jf = 'P3/2'

    # hyperfine transitions
    freqs_arr = [
            get_transition_freq(atom, Ji, Jf, 2, 3),
            get_transition_freq(atom, Ji, Jf, 2, 3),
            get_transition_freq(atom, Ji, Jf, 3, 2),
            get_transition_freq(atom, Ji, Jf, 3, 3)
            ]

    if add_crossover_transitions:
        # add cross-over transitions
        freqs_arr.extend([
             (freqs_arr[0]+freqs_arr[1])/2.0,     
             (freqs_arr[2]+freqs_arr[3])/2.0,     
            ])

    return np.sort(np.array(freqs_arr))


#####################################################################

def get_Rb85_calibration_intervals(laser_center_freq, scan_width = 20.0e6, df = 1.0e6):

    # gets list of frequencies
    abs_freqs = get_Rb85_calibration_transitions()

    no_of_points = int(scan_width/df)

    scan_interval = []

    for f in abs_freqs:
        hlp_interval = np.linspace(f - df, f + df, no_of_points)

        scan_interval.extend( hlp_interval - laser_center_freq )

    # return values in MHz
    return np.array(scan_interval)/1e6




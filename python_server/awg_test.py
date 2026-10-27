import numpy as np 
import matplotlib.pyplot as plt

###########################
# define linear ramp
###########################

def linear_ramp(t, start, stop, duration):

    return np.array(start + (stop - start)/duration * t)


def create_arb_wave(
        t, 
        start_freq, 
        end_freq, 
        start_amp,
        stop_amp,
        duration
        ):

    # get linear A ramp - might need to change to other type of ramp    
    A_ramp = linear_ramp(t, start_amp, stop_amp, duration)
    
    # get linear frequency ramp
    f_ramp = linear_ramp(t, start_freq, stop_freq, duration)

    # define arb wave	 
    y = A_ramp * np.sin( 2*np.pi * f_ramp * t )

    return y


###############################
# Main
###############################

MHz = 1e6

start_freq = 20*MHz
stop_freq = 500*MHz

start_amp = 140e-3 # mV
stop_amp = 640e-3 

duration = 100e-9 

#what wave do I need for Mn MOT? A frequency and amplitude chirp.
num__points = 16384
#t = np.linspace(0, 1, num__points, endpoint = False)

t0 = np.linspace(0, duration, 1000)

y = create_arb_wave(t0, start_freq, stop_freq, start_amp, stop_amp, duration)

plt.plot(t0, y)





plt.show()





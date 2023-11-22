#!/usr/bin/env python3

import time
from furnace import Furnace
from raspi   import Raspi

#############################
# Main
#############################

time_interval = 10 # in seconds
    
f = Furnace(dummy = True)

f.stop()

# set pattern
f.prg_pattern(0, T_arr = [20, 150, 20, 0, 0, 0, 0], time_arr = [1, 60, 60, 0, 0, 0, 0])

f.set_pattern(0)

# start furnace
f.start()

no_of_cycles = int(1.1 * f.get_run_time() / time_interval)

for k in range(no_of_cycles):

    # read out current temperature of furnace
    f.monitor_furnace()

    f.print_status()

    # send trigger to spectrometer
    raspi.trigger()

    time.sleep(time_interval)

f.stop()



#!/usr/bin/python3

import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot
import time
import numpy as np

from simple_pid import PID


setpoint = 12.0

trigger_threshold = 0.2

pid = PID(0, 2e-2, 0, setpoint = setpoint)

pid.sample_time = 0.5
#pid.auto_mode = False

pid.output_limits = (-1, 1)

#rp_s = scpi.scpi(sys.argv[1])
rp_s = scpi.scpi('192.168.42.52')

rp_s.rst()

wave_form = 'SAWU'



freq = 50
ampl = 1.0
offset = 0.0
 
if True:


    #####################################
    # Signal generator
    #####################################

    rp_s.tx_txt('GEN:RST')
     
    rp_s.tx_txt('SOUR1:FUNC ' + str(wave_form).upper())
    rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
    rp_s.tx_txt('SOUR1:VOLT:OFFS ' + str(offset))
    rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))
    
    rp_s.tx_txt('SOUR1:BURS:STAT BURST')        # Set burst mode to CONTINUOUS/skip this section for sine wave generation on External trigger
    
    rp_s.tx_txt('SOUR1:BURS:NCYC 1')

    rp_s.tx_txt('SOUR1:TRIG:SOUR EXT_PE')
    
    rp_s.tx_txt('OUTPUT1:STATE ON')



    #####################################
    # Photodiode detection
    #####################################

    fac = 1.0/2.0
    decimation = 0.5*1024
    buffer_size = int(fac*16384)

    trigger_delay = 6*1000 #int(fac*8000) # in samples





    time_max = buffer_size * 1.0/(125e6/decimation)

    times = np.linspace(0, time_max, buffer_size)

    rp_s.tx_txt('ACQ:RST')

    rp_s.tx_txt('ACQ:DATA:FORMAT ASCII')
    rp_s.tx_txt('ACQ:DATA:UNITS VOLTS')
    rp_s.tx_txt('ACQ:DEC ' + str(decimation))
    
    rp_s.tx_txt('ACQ:TRIG:DLY ' + str(trigger_delay))
    

print('starting')

while 1:

#for k in range(3):

    rp_s.tx_txt('ACQ:TRIG EXT_PE')
    rp_s.tx_txt('ACQ:START')
    
    
    while 1:
        rp_s.tx_txt('ACQ:TRIG:STAT?')
        if rp_s.rx_txt() == 'TD':
            rp_s.tx_txt('ACQ:STOP')
            break

    rp_s.tx_txt('ACQ:SOUR1:DATA:OLD:N? ' + str(buffer_size))
    
    buff_string = rp_s.rx_txt()
    
    buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
    buff = np.array(list(map(float, buff_string)))
 

    # find position of threshold

    ind = np.where(buff > trigger_threshold)

    try:
        pid.auto_mode = True

        ind = ind[0][0]

        curr_pulse_time = times[ind]*1e3

        if curr_pulse_time > 10.0:

            print(curr_pulse_time)
    
            control = pid(curr_pulse_time)
    
            print(control)
    
            offset = -control
    
            rp_s.tx_txt('SOUR1:VOLT:OFFS ' + str(offset))
            
            #pid.auto_mode = False
        else:
            pid.auto_mode = False
    except:
        ind = 0

        pid.auto_mode = False



rp_s.close()



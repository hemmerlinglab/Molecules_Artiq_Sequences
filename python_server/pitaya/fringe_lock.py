#!/usr/bin/python3

import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plt
import time
import numpy as np

from simple_pid import PID


# converts list of numbers into comma-separated .5f string
conv2pitaya = lambda y : ", ".join(map(str, ["{0:.5f}".format(n) for n in y]))









setpoint = 12.0

trigger_threshold = 0.3

pid = PID(0, 2e-2, 0, setpoint = setpoint)

pid.sample_time = 0.5
#pid.auto_mode = False

pid.output_limits = (-1, 1)

#rp_s = scpi.scpi(sys.argv[1])
rp_s = scpi.scpi('192.168.42.52')

rp_s.rst()

wave_form = 'SAWU'



freq = 25#50
ampl = 1.0
offset = 0.0
 
fac = 1.0/2.0
decimation = 0.5*1024
buffer_size = int(fac*16384)

trigger_delay = 8192 #6*1000 #int(fac*8000) # in samples

if True:


    #####################################
    # Signal generator
    #####################################

    rp_s.tx_txt('GEN:RST')
     
    rp_s.tx_txt('SOUR1:FUNC ARBITRARY')
    rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
    #rp_s.tx_txt('SOUR1:VOLT:OFFS ' + str(offset))
    rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))
    
    rp_s.tx_txt('SOUR1:BURS:STAT BURST')        
    
    rp_s.tx_txt('SOUR1:BURS:NCYC 1')

    rp_s.tx_txt('SOUR1:TRIG:SOUR EXT_PE')
    #rp_s.tx_txt('SOUR1:TRIG:SOUR INT')
    #rp_s.tx_txt('SOUR1:TRIG:INT')
    
    rp_s.tx_txt('OUTPUT1:STATE ON')

    t = np.linspace(0, 1, buffer_size)
    #y = (1) * t
    times_ramp = t/freq/2.0

    ## waveform
    #rp_s.tx_txt('SOUR1:TRAC:DATA:DATA ' + conv2pitaya(y))

    #####################################
    # Photodiode detection
    #####################################





    time_max = buffer_size * 1.0/(125e6/decimation)

    times = np.linspace(0, time_max, buffer_size)

    rp_s.tx_txt('ACQ:RST')

    rp_s.tx_txt('ACQ:DATA:FORMAT ASCII')
    rp_s.tx_txt('ACQ:DATA:UNITS VOLTS')
    rp_s.tx_txt('ACQ:DEC ' + str(decimation))
    
    rp_s.tx_txt('ACQ:TRIG:DLY ' + str(trigger_delay))
    



d = []
ramps = []

no_of_shots = 5

print('starting')

ind = [[500]]
for k in range(no_of_shots):
#while 1:

    # full ramp
    y = (1) * 2.0 * t

    # get value of ramp amplitude
    #trig_time = times[ind[0][0]]

    try:
    #if True:

        trig_time = times[ind[0][0]]
        ind_hold = np.where( np.abs(times_ramp - trig_time) < 1e-5 )
        
        ind_hold = ind_hold[0][0]

        ramp_voltage = y[ind_hold]
        
        steps = 2000

        # ramp down
        # y[int(buffer_size/2):int(buffer_size/2)+steps] = 1.0 - (1.0 - ramp_voltage)/1.0 * np.linspace(0, 1, steps)
        
        # ramp up
        y[int(buffer_size/2):int(buffer_size/2)+steps] = ramp_voltage * np.linspace(0, 1, steps)

        t_remain = np.linspace(0, 1, len(y) - (int(buffer_size/2)+steps))
        y[int(buffer_size/2)+steps:] = ramp_voltage + 0.025 * np.sin(300*t_remain)

    except:
        pass

    ## hold ramp
    #y[int(buffer_size/2):] = 2.0 * t[0:int(buffer_size/2)]
   
    ##try:
    #if True:
    #    
    #    trig_time = times[ind[0][0]]
    #    guess_time = trig_time + 0.25/freq
    #    
    #    print('here')
    #    print('trig @ {0}; trig shift @ {1}'.format(1e3*trig_time, 1e3*guess_time))
    #    
    #    print(times_ramp*1e3)

    #    ind_hold = np.where( np.abs(times_ramp - (times[ind[0][0]] + 0.25 * 1/freq)) < 1e-4 )
    #    
    #    ind_hold = ind_hold[0][0]
    #    
    #    print('ramp trig @ {0}'.format(1e3*times_ramp[ind_hold]))

    #    y[ind_hold:] = y[ind_hold]

    ##except:
    ##    pass


    



    rp_s.tx_txt('SOUR1:TRAC:DATA:DATA ' + conv2pitaya(y))
    
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

    d.append(buff)

    ramps.append(y)
    
    
    #y = (1) * t

    #try:
    #    ind = ind[0][0]
    #    y[ind:] = y[ind]
    #except:
    #    ind = 0        



    ## waveform
    #rp_s.tx_txt('SOUR1:TRAC:DATA:DATA ' + conv2pitaya(y))
    #time.sleep(0.025) 
    #rp_s.tx_txt('SOUR1:TRIG:SOUR INT')
    #rp_s.tx_txt('SOUR1:TRIG:INT')



    #try:
    #    pid.auto_mode = True

    #    ind = ind[0][0]

    #    curr_pulse_time = times[ind]*1e3

    #    if curr_pulse_time > 10.0:

    #        print(curr_pulse_time)
    #
    #        control = pid(curr_pulse_time)
    #
    #        print(control)
    #
    #        offset = -control
    #
    #        rp_s.tx_txt('SOUR1:VOLT:OFFS ' + str(offset))
    #        
    #        #pid.auto_mode = False
    #    else:
    #        pid.auto_mode = False
    #except:
    #    ind = 0

    #    pid.auto_mode = False



rp_s.close()

d = np.array(d)
d = np.transpose(d)

ramps = np.array(ramps)
ramps = np.transpose(ramps)


for k in range(no_of_shots):

    plt.figure()

    plt.plot(times*1e3, d[:, k])
    #plt.plot(np.arange(buffer_size)/freq * 1e3 * 1.0/(125e6/decimation), ramps[:, k])
    plt.plot(times_ramp * 1e3, ramps[:, k])

plt.show()


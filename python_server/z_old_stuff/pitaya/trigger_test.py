#!/usr/bin/python3

import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot
import time
import numpy as np


#rp_s = scpi.scpi(sys.argv[1])
rp_s = scpi.scpi('192.168.42.52')

rp_s.rst()

wave_form = 'SAWU'


freq = 100
ampl = 1.0
offset = 0.0
 
if True:


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
    # photodiode detection
    #####################################

    fac = 1.0/2.0
    decimation = 0.5*1024
    buffer_size = int(fac*16384)

    trigger_delay = 6*1000 #int(fac*8000) # in samples

    trigger_threshold = 0.045




    time_max = buffer_size * 1.0/(125e6/decimation)

    times = np.linspace(0, time_max, buffer_size)

    rp_s.tx_txt('ACQ:RST')

    rp_s.tx_txt('ACQ:DATA:FORMAT ASCII')
    rp_s.tx_txt('ACQ:DATA:UNITS VOLTS')
    rp_s.tx_txt('ACQ:DEC ' + str(decimation))
    
    rp_s.tx_txt('ACQ:TRIG:DLY ' + str(trigger_delay))
    #rp_s.tx_txt('ACQ:TRIG:LEV ' + str(trigger_threshold))
    

print('starting')

while 1:

#for k in range(3):

    rp_s.tx_txt('ACQ:TRIG EXT_PE')
    #rp_s.tx_txt('ACQ:TRIG CH1_PE')
    rp_s.tx_txt('ACQ:START')
    
    
    while 1:
        rp_s.tx_txt('ACQ:TRIG:STAT?')
        if rp_s.rx_txt() == 'TD':
            rp_s.tx_txt('ACQ:STOP')
            break

    #rp_s.tx_txt('ACQ:SOUR1:DATA?') # read full buffer
    
    #rp_s.tx_txt('ACQ:SOUR1:DATA:STA:N? 10,' + str(buffer_size))
    #rp_s.tx_txt('ACQ:SOUR1:DATA:OLD:N? ' + str(buffer_size))

    rp_s.tx_txt('ACQ:SOUR1:DATA:OLD:N? ' + str(buffer_size))
    
    buff_string = rp_s.rx_txt()
    
    buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
    buff = np.array(list(map(float, buff_string)))
 

    # find position of threshold

    ind = np.where(buff > trigger_threshold)

    try:
        ind = ind[0][0]

        print(times[ind]*1e3)

    except:
        ind = 0

    #rp_s.tx_txt('ACQ:TPOS?')
    #trig_pos = rp_s.rx_txt()

    #rp_s.tx_txt('ACQ:WPOS?')

    #write_pos = rp_s.rx_txt()
    #
    ##print('delay:' + str(abs(float(trig_pos) - float(write_pos) ) ) )
    #print('trig_pos: {1:5.0f}, write_pos: {2:5.0f}, delay: {0:5.0f}\n'.format(float(trig_pos) - float(write_pos), float(trig_pos), float(write_pos)))

    #rp_s.tx_txt('ACQ:TRIG:DLY?')
    #trig_pos = rp_s.rx_txt()

    #print("delay" + str(trig_pos))

    #rp_s.tx_txt('OUTPUT1:STATE OFF')

    plot.plot(times*1e3, buff)
    #plot.text(0.5,0.5,str(trig_pos))
    
    plot.axvline(times[ind]*1e3)
    #plot.axhline(0.4)
    #plot.axvline(trig_pos+write_pos)
    plot.xlabel('Time (ms)')
    plot.ylabel('Voltage')
    plot.show()

    #time.sleep(0.25)
    
    #rp_s.tx_txt('OUTPUT1:STATE OFF')


rp_s.close()



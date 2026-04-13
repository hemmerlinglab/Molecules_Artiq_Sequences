#!/usr/bin/python3

import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plt
import time
import numpy as np

from simple_pid import PID


# converts list of numbers into comma-separated .5f string
conv2pitaya = lambda y : ", ".join(map(str, ["{0:.5f}".format(n) for n in y]))





rp_s = scpi.scpi('192.168.42.52')

rp_s.rst()




#wave_form = 'sine'
#freq = 2000
#ampl = 1
#
#rp_s.tx_txt('GEN:RST')
#
#rp_s.tx_txt('SOUR1:FUNC ' + str(wave_form).upper())
#rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
#rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))
#
## Enable output
#rp_s.tx_txt('OUTPUT1:STATE ON')
#rp_s.tx_txt('SOUR1:TRIG:INT')
#
#
#
#asd


freq = 50
ampl = 1.0
offset = 0.0
 
fac = 1.0/2.0
decimation = 0.5*1024
buffer_size = int(fac*16384)

trigger_delay = 6*1000 #int(fac*8000) # in samples

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

    t = np.linspace(0,1,buffer_size)
    y = (1) * t

    # waveform
    rp_s.tx_txt('SOUR1:TRAC:DATA:DATA ' + conv2pitaya(y))

    
    rp_s.tx_txt('OUTPUT1:STATE ON')
    
#    rp_s.tx_txt('SOUR1:TRIG:INT')




##print('starting')
##
###for k in range(3):
while 1:
##
##    #rp_s.tx_txt('SOUR1:TRIG:SOUR EXT_PE')
    rp_s.tx_txt('SOUR1:TRIG:INT')

    time.sleep(0.2)
##
##    y = (1) * t
##    rp_s.tx_txt('SOUR1:TRAC:DATA:DATA ' + conv2pitaya(y))
    


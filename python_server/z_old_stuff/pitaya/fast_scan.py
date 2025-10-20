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

wave_form = 'SAWU'



freq = 1500
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
     
    rp_s.tx_txt('SOUR1:FUNC SAWU')
    rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
    rp_s.tx_txt('SOUR1:VOLT:OFFS ' + str(offset))
    rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))
    
    rp_s.tx_txt('SOUR1:BURS:STAT BURST')        
    
    rp_s.tx_txt('SOUR1:BURS:NCYC 3')

    rp_s.tx_txt('SOUR1:TRIG:SOUR EXT_PE')
    
    rp_s.tx_txt('OUTPUT1:STATE ON')



print('starting')


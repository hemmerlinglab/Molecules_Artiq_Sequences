#!/usr/bin/python

import sys
import time
import redpitaya_scpi as scpi

#rp_s = scpi.scpi(sys.argv[1])

rp_s = scpi.scpi('192.168.42.52')

#if (len(sys.argv) > 2):
#    led = int(sys.argv[2])
#else:
#    led = 0

led = 4

print ("Blinking LED["+str(led)+"]")

period = 1 # seconds

while 1:
    time.sleep(period/2.0)
    rp_s.tx_txt('DIG:PIN LED' + str(led) + ',' + str(1))
    time.sleep(period/2.0)
    rp_s.tx_txt('DIG:PIN LED' + str(led) + ',' + str(0))




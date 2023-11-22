#!/usr/bin/python3

import time

import RPi.GPIO as io # using RPi.GPIO

io.setmode(io.BCM)

io.setup(4,io.OUT) # make pin into an output


while True:

    print('Trigger')
    time.sleep(1)

    io.output(4,1)
    
    time.sleep(0.1)

    io.output(4,0)
    
    time.sleep(5)
 


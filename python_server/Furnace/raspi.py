#!/usr/bin/python3

import RPi.GPIO as io # using RPi.GPIO

class Raspi():

    def __init__(self, trigger_length = 0.1):

        io.setmode(io.BCM)

        io.setup(4,io.OUT) # make pin into an output

        self.trigger_length = trigger_length

        return

    def trigger(self):

        print('Sending trigger ...')

        io.output(4,1)
    
        time.sleep(self.trigger_length)

        io.output(4,0)

        return



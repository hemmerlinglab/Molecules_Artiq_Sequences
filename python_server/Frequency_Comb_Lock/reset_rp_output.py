#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import socket
import sys
import os

from koheron import connect
from fft import FFT


def conv2bit(V):

    # Converts the +/- 1V of the red pitaya outputs to a 14-bit (15th bit is used for the sign)

    if V >= 0:
        my_bits = int( (2**15 - 1) * V )
    else:
        my_bits = int( 2**16 - 2**15 * abs(V) )

    return my_bits


def RP():
    # initializes RP

    host = os.getenv('HOST', '192.168.42.53')
    client = connect(host, 'fft', restart=False)
    driver = FFT(client)

    driver.set_input_channel(1)
    #driver.set_output(conv2bit(0))

    return driver

   

rp  = RP()

rp.set_output(conv2bit(0.0))


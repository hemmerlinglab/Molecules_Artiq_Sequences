import socket
import time
import numpy as np

import matplotlib.pyplot as plt

import pyvisa as visa

class Rigol_DSG821:
    
    def __init__(self):

        rm = visa.ResourceManager("@py")

        self.dev = rm.open_resource('TCPIP::192.168.42.46::INSTR')

        return

    def send(self, msg):

        self.dev.write(msg)

        return

    def query(self, msg):

        return self.dev.query(msg)

    def set_freq(self, freq):

        self.dev.write(':FREQ {0}MHz'.format(float(freq)))

        return

    def set_level(self, level):

        self.dev.write(':LEV {0}'.format(float(level)))

        return

    def on(self):

        self.dev.write(':OUTP ON')

        return

    def off(self):

        self.dev.write(':OUTP OFF')

        return

    def close(self):

        self.dev.close()

        return


import serial
import os
import datetime
import time

from instrument import Instrument


def check_default(opts, key, default_val):

    # checks if the parameter is set, if not return the default_val

    if key in opts.keys():
        return opts[key]
    else:
        return default_val


class RS232_Instrument(Instrument):

    def __init__(self, opts):

        super().__init__()

        self.serial_port = opts['serial_port']
        self.baud_rate   = opts['baud_rate']
        
        self.msg_end     = check_default(opts, 'msg_end', '\r\n')

        self.device = serial.Serial(
                               self.serial_port, 
                               self.baud_rate, 
                               bytesize  = check_default(opts, 'bytesize', serial.SEVENBITS), 
                               parity    = check_default(opts, 'parity',   serial.PARITY_ODD), 
                               stopbits  = check_default(opts, 'stopbits', serial.STOPBITS_ONE), 
                               xonxoff   = check_default(opts, 'xonxoff',  False), 
                               rtscts    = check_default(opts, 'rtscts',   False), 
                               timeout   = 1
                               )

        if opts['open']:
            self.open()

        self.answer = None

        print(self.device)

        return

    def open(self):

        if self.device.isOpen():
            self.flush()
        else:
            self.device.open()
        
        return
    
    def flush(self):

        self.device.flushInput()
        self.device.flushOutput()

        return

    def query(self, cmd, sleep = 0, multilines = False, length = None):

        self.device.write(bytes(cmd + self.msg_end, 'utf-8'))
    
        if sleep > 0:
            time.sleep(sleep)

        if multilines:
            self.msg = self.device.readlines()
        else:
            self.msg = self.device.readline().decode('utf-8')
 
        return self.msg

    def read(self, multilines = False):

        if multilines:
            self.msg = self.device.readlines()
        else:
            self.msg = self.device.readline().decode('utf-8')
 
        return self.msg

    def read_sensor(self):
        
        return

    def print_answer(self):

        print(self.answer)

        return


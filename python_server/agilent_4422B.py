import serial
import os
import datetime
import time

from rs232_instrument import RS232_Instrument

class Agilent_E4422B(RS232_Instrument):

    def __init__(self):

        self.opts = { 'device' : {
                                'serial_port' : '/dev/Agilent_E4422B',
                                'baud_rate'   : 19200,
                                'bytesize'    : serial.EIGHTBITS,
                                'parity'      : serial.PARITY_ODD,
                                #'parity'      : serial.PARITY_NONE,
                                'stopbits'    : serial.STOPBITS_ONE,
                                'xonxoff'     : False,
                                'rtscts'      : True,
                                'msg_end'     : '\r\n',
                                'open'        : True
                            },
               }

        # init instrument
        RS232_Instrument.__init__(self, self.opts['device'])

        return

    def info(self):

        return self.query('*IDN?')


############################################################

if __name__ == '__main__':

    instr = Agilent_E4422B()

    print(instr.info())

    instr.close()





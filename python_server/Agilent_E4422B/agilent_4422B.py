import serial
import os
import datetime
import time

from base_instruments import base_gpib_instrument

class Agilent_E4422B(base_gpib_instrument):

    def __init__(self):

        self.opts = { 'device' : {
                                'IP'          : 19,
                                'msg_end'     : '\r\n',
                                'open'        : True
                            },
               }

        # init instrument
        base_gpib_instrument.__init__(self, self.opts['device']['IP'])

        return

    def get_fm_status(self):
    
        fm1_dev   = self.query('FM1:DEV?')
        fm1_cpl   = self.query('FM1:SOURCE?')
        fm1_state = self.query('FM1:STATE?')

        return

    def get_device_state(self):

        print(self.query('AM1:STATE?'))
        print(self.query('AM2:STATE?'))

        freq = self.query('FREQ?')

        print(freq)
        
        f = 85.00e6
        self.write('FREQ {0}Hz'.format(f))

        freq = self.query('FREQ?')

        print(freq)
        
        self.write('OUTPUT:STATE OFF')
        
        self.write('OUTPUT:MODULATION:STATE OFF')
       
        lvl = -12.50
        self.write('POWER:LEVEL:IMM:AMPLITUDE {0}DBM'.format(lvl))
        
 
        return


############################################################

if __name__ == '__main__':

    instr = Agilent_E4422B()

    instr.id()

    instr.get_device_state()

    instr.close()





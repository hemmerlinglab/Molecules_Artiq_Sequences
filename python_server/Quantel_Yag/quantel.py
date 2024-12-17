import serial
import os
import datetime
import time

from rs232_instrument import RS232_Instrument

class Quantel_Yag(RS232_Instrument):

    def __init__(self):

        self.opts = { 'device' : {
                                'serial_port' : '/dev/QuantelYag_USB',
                                'baud_rate'   : 9600,
                                'bytesize'    : serial.EIGHTBITS,
                                #'parity'      : serial.PARITY_ODD,
                                'parity'      : serial.PARITY_NONE,
                                'stopbits'    : serial.STOPBITS_ONE,
                                'xonxoff'     : False,
                                'rtscts'      : False,
                                #'dsrdtr'      : True,
                                'msg_end'     : '\r\n',
                                'open'        : True
                            },
               }

        # init instrument
        RS232_Instrument.__init__(self, self.opts['device'])

        return

    def info(self):

        return "{0}".format(self.query('>x'))

    def get_par(self, par):

        return self.query('>{0}'.format(par))

    def diag(self):

        pars = ['cg',
                'p', # pump
                'wor',
                #'if',
                'vis',
                'vos', # calibration factor, % of vmo setting
                'vmo',
                'v',
                'va',
                #'vt',
                'd',
                'e',
                'ene',
                'f',
                'w',
                'c',
                'cap',
                'lpm',
                'qsm',
                'qsf',
                'qsp',
                'qof',
                'cq',
                'r', # shutter
                ]

        status = {}
        for k in pars:
            status[k] = self.get_par(k)

        # print output
        print()
        print('Quantel status')
        print('*' * 30)
        for k in status.keys():
            print('{0:5} : {1}'.format(k, status[k]))
        print('*' * 30)
        print()

        return

    def test_safety_interlocks(self):

        # test safety flashlamp
        print('{0}'.format(self.query('>if1')))
        
        print('{0}'.format(self.query('>if2')))

        # test safety q-switch
        print('{0}'.format(self.query('>iq')))
        
        # test temperature HG
        print('{0}'.format(self.query('>ihg')))

        return

    def flashlamp_autofire(self):

        # switch on auto fire for the flashlamp
        self.query('>a')

        return

    def fast_warm_up(self):

        self.flashlamp_autofire()

        return

    def set_qdelay(self, q_delay):

        q_delay = max(100.0, q_delay)
        q_delay = min(999.0, q_delay)

        self.query('>w{0:.0f}'.format(q_delay))

        return

    def set_f_rep(self, x):

        x = max(1.0, x)
        x = min(100.0, x)

        self.query('>f{0:.0f}'.format(x * 100.0))

        return

    def set_ene(self, x):

        x = max(7.0, x)
        x = min(20.0, x)

        self.query('>ene{0:.0f}'.format(x * 10.0))

        return

    def set_vmo(self, x):

        x = max(500.0, x)
        x = min(1150.0, x)

        self.query('>vmo{0:.0f}'.format(x))

        return

    def set_vis(self, x):

        x = max(0.0, x)
        x = min(100.0, x)

        self.query('>vis{0:.0f}'.format(x))

        return

    def set(self, ene = 12.0, f_rep = 1.0, q_delay = 140):

        self.set_ene(ene)

        self.set_f_rep(f_rep)

        self.set_qdelay(q_delay)

        return

    def on(self):
       
        # open shutter
        self.open_shutter()

        print('Activating q-switch')
        # switch on q-switch
        self.query('>pq')
        
        return

    def off(self):
        
        print('Deactivating q-switch')
        # switch on q-switch
        self.query('>sq')
         
        # close shutter
        self.close_shutter()
       
        return

    def standby(self):

        print('Laser in standby')

        self.query('>s')
        
        self.close_shutter()

        return

    def open_shutter(self):

        print('Opening shutter')
        self.query('>r1')

        return

    def close_shutter(self):
        
        print('Closing shutter')
        self.query('>r0')

        return


############################################################

if __name__ == '__main__':

    instr = Quantel_Yag()

    instr.diag()
    
    instr.close_shutter()

    instr.test_safety_interlocks()

    instr.flashlamp_autofire()

    #for k in range(30):
    #    instr.open_shutter()
    #    time.sleep(1)
    #    instr.close_shutter()
    #    time.sleep(1)

    instr.close()

    asd

    instr.diag()
        
    instr.fast_warm_up()

    instr.diag()

    instr.set(ene = 12.5, f_rep = 30.0, q_delay = 140)

    instr.set_vmo(1150)
   
    #instr.set(ene = 12.5, f_rep = 1.0, q_delay = 140)
    
    instr.on()

    instr.set_vis(0)
    instr.set_vis(100)
 
    instr.diag()
    
    time.sleep(3)

    instr.off()
    
    instr.standby()
    
    instr.diag()

    instr.close()




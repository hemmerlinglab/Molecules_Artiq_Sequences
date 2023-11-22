#!/usr/bin/env python3

import serial
import os
import datetime
import time
import binascii
import numpy as np
import minimalmodbus




def conv(s):
    # converts a hex string to binary    

    val = [ int(s[k]) * 16**(len(s)-1 - k) for k in range(len(s))]

    return sum(val)



class Dummy_Instrument():

    def __init__(self):

        return

    def read_register(self, x):

        print('Reading register {0}'.format(x))

        return 0.0

    def write_register(self, x, y):

        print('Writing to register {0}: {1}'.format(x, y))

        return 0.0


    def write_bit(self, x, y):

        print('Writing to bit {0}: {1}'.format(x, y))

        return



class Furnace():

    def __init__(self, dummy = False):

        if dummy == False:

            PORT = '/dev/Furnace'
        
            instrument = minimalmodbus.Instrument(PORT,1,mode=minimalmodbus.MODE_RTU)
            
            #Make the settings explicit
            instrument.serial.baudrate = 9600        # Baud
            instrument.serial.bytesize = 8
            instrument.serial.parity   = minimalmodbus.serial.PARITY_EVEN
            instrument.serial.stopbits = 1
            instrument.serial.timeout  = 1          # seconds
            
            # Good practice
            instrument.close_port_after_each_call = True
            
            instrument.clear_buffers_before_each_transaction = True

            self.device = instrument

        else:

            self.device = Dummy_Instrument()

        return

    def get_tact(self):

        self.tact = 0.1 * self.device.read_register( conv('1000') )

        return self.tact

    def get_tset(self):

        self.tset = 0.1 * self.device.read_register( conv('1001') )

        return self.tset

    def start(self):

        self.device.write_bit( conv('0814'), 1 )

        return

    def stop(self):

        self.device.write_bit( conv('0814'), 0 )

        return

    def set_pattern(self, no):

        self.device.write_register( conv('1030'), int(no) )

        return

    def prg_pattern(self, no, T_arr = [], time_arr = []):

        offset_T    = 2 * 16**3             # 2000H
        offset_time = 2 * 16**3 + 8 * 16**1 # 2080H

        for k in range(len(T_arr)):

            T_register = offset_T + no*8 + k 

            self.device.write_register( T_register, int(10*T_arr[k]) ) # T_arr needs to be in 0.1 deg C
            
            time_register = offset_time + no*8 + k 
            
            self.device.write_register( time_register, int(time_arr[k]) )

        self.total_run_time = np.sum(time_arr)

        return
   
    def get_run_time(self):

        return self.total_run_time

    def get_output(self):

        self.output = self.device.read_register( conv('1012') )

        return self.output


    def monitor_furnace(self):

        # get timestamp
        my_today = datetime.datetime.today()
        current_time_stamp = str(my_today.strftime('%Y/%m/%d-%H:%M:%S'))
        
        # get set value
        Tset = self.get_tset()
        
        # get act value        
        Tact = self.get_tact()
        
        # get output
        out = self.get_output()

        log_entry = current_time_stamp + ',Tset,' + str(Tset) + ',Tact,' + str(Tact) + ',out,' + str(out)
       
        # save data
        self.logfilename = '~/furnace_data/furnace_log.csv'

        # open file and append if already exists
        if os.path.isfile(self.logfilename):
            self.log_file = open(self.logfilename, 'a')
        else:    
            self.log_file = open(self.logfilename, 'w')

        self.log_file.write(log_entry + "\n")

        self.log_file.close()

        print(log_entry)

        return


##############################
## Main
##############################
#
#if __name__ == '__main__':
#    
#    f = Furnace()
#
#    f.stop()
#
#    f.prg_pattern(0, [20, 60, 20, 0, 0, 0, 0], [1, 20, 20, 0, 0, 0, 0])
#   
#    print(f.get_run_time())
#
#    f.set_pattern(0)
#
#    f.start()
#
#    for k in range(1000):
#
#        f.monitor_furnace()
#
#        time.sleep(1)
#
#    f.stop()



import socket
import time
import numpy as np

import matplotlib.pyplot as plt


class Keysight:
    
    def __init__(self):

        TCP_IP = '192.168.42.63'
        TCP_PORT = 5025

        self.command_delay = 0.01

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        s.connect((TCP_IP,TCP_PORT))
    
        s.send(b"*IDN?\n")
        t = s.recv(1024)
    
        #print(t)
        
        self.socket = s
    

    def send(self, msg):

        send_msg = msg + '\n'

        self.socket.send(send_msg.encode())

        time.sleep(self.command_delay)

    def recv(self):

        self.msg = self.socket.recv(1024)

        return self.msg

    def query(self, msg, number_of_bytes = 1024):

        self.send(msg)

        self.msg = self.socket.recv(number_of_bytes)

        self.msg = self.msg.decode().strip('\n')

        return self.msg


    def set_center_freq(self, freq):

        self.send(':FREQ:CENT ' + str(freq) + ' Hz')

    def set_span(self, span):

        self.send(':FREQ:SPAN ' + str(span) + ' Hz')

    def marker_on(self, no):

        self.send(':CALC:MARK' + str(no) + ':STATE ON')

    def get_trace(self):

        #print('Getting trace')
        #
        #
        ##my_format = (self.query('FORMAT:TRACE:DATA?'))

        #print(no_of_points)
        ##print(my_format)

        ##d = self.query(':TRACE:DATA? TRACE1', number_of_bytes = 17*no_of_points)

        no_of_points = int(self.query('SENS:SWE:POIN?'))
        
        #print(no_of_points)
        no_of_points = 821

        d = self.query(':TRACE:DATA? TRACE1', number_of_bytes = 17*no_of_points)
        
        d = d + self.query(':TRACE:DATA? TRACE1', number_of_bytes = 17*no_of_points)
        
        d = d.strip(',')
       
        #print(len(d)/17)
        d2 = np.array([float(x) for x in d.split(',')])
        
        return d2[:-1]


    def set_sweep(self):

        
        self.send(':TRACE:CLE TRACE1')

        self.send(':INIT:CONT OFF')
        
        self.query('*OPC?')
       
        self.send(':INIT:IMM')
        
        self.query('*OPC?')
        
        return 



    def marker_measure(self, no, wait_time = None):

        self.send(':CALC:MARK' + str(no) + ':MAX')

        if not wait_time is None:
            time.sleep(wait_time)

        x = self.query(':CALC:MARK' + str(no) + ':X?')
        
        y = self.query(':CALC:MARK' + str(no) + ':Y?')        
        
        err = self.query(':SYST:ERR?')        

        return (np.float64(x), np.float64(y), err)

    def close(self):

        self.socket.close()







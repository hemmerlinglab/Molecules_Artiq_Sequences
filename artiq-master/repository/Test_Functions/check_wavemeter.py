# use 'artiq-run' command
#from artiq.experiment import *

import os
import sys
import time
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions")
import socket

import numpy as np
#from my_instrument_functions    import calibrate_wavemeter, get_wavemeter_readings

#######################################################################################################

def calibrate_wavemeter(freq):

    # calibrates wavemeter

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.42.20', 62200)

    sock.connect(server_address)

    # 'request' gets only one frequency
    try:    
        # Request data
        message = 'calibra'
        #print('sending "%s"' % message)
        sock.sendall(message.encode())

        message = "{0:.6f}".format(float(freq))
        
        sock.sendall(message.encode())


    finally:
        sock.close()
 
    
    return 



#######################################################################################################

def get_wavemeter_readings(mode = 'wavemeter_lock'):

    # reads out laser frequencies from wavemeter

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.42.20', 62200)

    sock.connect(server_address)

    if mode == 'wavemeter_lock':
        # 'request' gets only one frequency
        try:    
            # Request data
            message = 'request'
            #print('sending "%s"' % message)
            sock.sendall(message.encode())

            len_msg = int(sock.recv(2).decode())

            data = sock.recv(len_msg)

        finally:
            sock.close()

        # return a list of freqs
        # currently only one frequency is returned
        freqs = [float(data.decode())]

    else:
        # 'request' gets only one frequency
        try:    
            # Request data
            message = 'reqch18'
            #print('sending "%s"' % message)
            sock.sendall(message.encode())

            len_msg = int(sock.recv(2).decode())

            data = sock.recv(len_msg)

        finally:
            sock.close()

        # return a list of freqs
        # currently only one frequency is returned
        freqs = data.decode().split(',')

        freqs = [ float(x) for x in freqs ]

    
    return freqs




###################################################################################
# Experiment
###################################################################################

if __name__=='__main__':

    delta = np.linspace(-200, 200, 10)
    
    base_freq = 384.228067e12
    
    results = []
    
    for d in delta:
    
        new_v = (base_freq + d * 1e6) / 1e12
    
        print('Calibrating to {0} THz'.format(new_v))
    
        calibrate_wavemeter(new_v)
    
        time.sleep(3)
    
        freqs = get_wavemeter_readings(mode = 'comb_lock')
    
        hlp = [new_v, freqs[0], freqs[1]]
    
        results.append(hlp)
    
    
    np.savetxt('wavemeter_check.csv', results, delimiter = ',')
    
    calibrate_wavemeter(base_freq/1e12)



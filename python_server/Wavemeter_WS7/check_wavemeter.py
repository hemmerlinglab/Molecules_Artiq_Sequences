import os
import socket
import sys
import numpy as np
import time

sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server")

from rigol               import Rigol_RSA3030

import matplotlib.pyplot as plt

# This script measures the wavemeter offset


from calibrate_wavemeter import get_comb_tooth, read_beatnode, show_status

###########################################
# Get wavemeter readings of Ch 2 and Ch 8
###########################################

def read_wavemeter_channel():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.42.20', 62200)

    sock.connect(server_address)

    try:    
        # Request data
        message = 'request'
 
        sock.sendall(message.encode())

        len_msg = int(sock.recv(2).decode())

        data = sock.recv(len_msg)

    finally:
        sock.close()

    freqs = float(data.decode())

    return freqs * 1e12 # in Hz


##########################################################################

def run_wavemeter_check():

    print('Getting wavemeter data')

    # get wavemeter readings
    (wm_moglabs) = read_wavemeter_channel()
    
    # get beatnode frequency
    freq_beat_node = read_beatnode()
    
    # calculate comb tooth
    (v_moglabs, n_comb) = get_comb_tooth(freq_beat_node, wm_moglabs)
    
    # show status and get offset of wavemeter from Moglabs measurements
    delta = show_status(0, wm_moglabs, v_moglabs, freq_beat_node, n_comb)

    print('-'*60)
    print('Scaled wavemeter offset for different ranges:')
    print()

    for k in np.arange(400, 1000, 100):
        nu = 299792458/(k*1e-9)
        print('{0} nm: {1:.0f} MHz'.format( k, nu/wm_moglabs * delta/1e6 ))
    
    print('-'*60)
    print()

    return 0




if __name__ == '__main__':

   run_wavemeter_check()




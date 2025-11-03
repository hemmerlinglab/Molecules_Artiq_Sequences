import os
import socket
import sys
import numpy as np
import time

sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server")

from rigol               import Rigol_RSA3030

import matplotlib.pyplot as plt

# This script calibrates the wavemeter by reading the frequency of Hodor and the comb beatnode

###########################################
# Get wavemeter readings of Ch 2 and Ch 8
###########################################

def read_wavemeter_channels():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.42.20', 62200)

    sock.connect(server_address)

    try:    
        # Request data
        message = 'reqch28'
 
        sock.sendall(message.encode())

        len_msg = int(sock.recv(2).decode())

        data = sock.recv(len_msg)

    finally:
        sock.close()

    freqs = data.decode().split(',')

    freqs = [ float(x) for x in freqs ]

    return (freqs[0] * 1e12, freqs[1] * 1e12) # in Hz


###########################################
# Get beatnode
###########################################

def read_beatnode():

    spec = Rigol_RSA3030()

    #spec.set_freq([2e6, 205e6])

    d = spec.get_trace()

    f = d[:, 0]

    s = d[:, 1]


    # get beat node

    # cut indices between 60 and 80 MHz
    ind = np.where( (f > 60e6) & (f < 90e6))[0]

    ind_c = min(ind) + np.where( s[ind] == max(s[ind]) )[0][0]

    plt.plot(f, s)
    plt.plot(f[ind], s[ind], 'r')
    plt.axvline(f[ind_c], color = 'g')    

    freq_beat_node = f[ind_c]

    return freq_beat_node
 

###########################################
# Get comb tooth
###########################################

def get_comb_tooth(freq_beat_node, v_wavemeter):

    vrep_nom = 200.0e6

    n = np.floor( v_wavemeter / vrep_nom )

    # true frequency

    v_true = n * vrep_nom + freq_beat_node

    return (v_true, n)


###########################################
# Show status
###########################################

def show_status(wm1, wm2, v_true, v_bn, n):

    
    print('''
TiSaph:                         {0:.6f} THz

Moglabs (wavemeter):            {1:.6f} THz
Moglabs (true):                 {2:.6f} THz
-------------------------------------------
Difference (true - wavemeter):  {3:.1f} MHz

beat node frequency {4:.1f} MHz
comb tooth n = {5:.0f}
'''.format(wm1/1e12, wm2/1e12, v_true/1e12, (v_true - wm2)/1e6, v_bn/1e6, n))
    
    return




##########################################################################

# get wavemeter readings
(wm_tisaph, wm_moglabs) = read_wavemeter_channels()

# get beatnode frequency
freq_beat_node = read_beatnode()

# calculate comb tooth
(v_moglabs, n_comb) = get_comb_tooth(freq_beat_node, wm_moglabs)

# show status
show_status(wm_tisaph, wm_moglabs, v_moglabs, freq_beat_node, n_comb)






plt.show()




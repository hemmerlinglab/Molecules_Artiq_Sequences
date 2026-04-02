import serial
import os
import datetime
import time
import socket
import sys
import numpy as np
import threading
import queue

from simple_pid import PID

from wlm import *
from Fiber import *

from network_tools import *


#############################################################
# Switch Fiber Channel
#############################################################

def switch_fiber_channel(opts, channel, wait_time = None, manual_switch = False):

    sock = connect_and_send_socket(opts['fiber_server_ip'], opts['fiber_server_port'], str(channel))
    
    sock.close()

    if not wait_time == None:
        time.sleep(wait_time)

    return 


#############################################################
# Init All Servers
#############################################################

def init_distribution_servers(opts):

    # init wavemeter
    wlm = WavelengthMeter()

    # init fiber switcher
    fib = Fiber(opts['fiber_switcher_com_port'])

    # init wavemeter servers
    dist_sockets = []
    for k in range(len(opts['dist_sockets'])):    

        dist_sockets.append(bind_socket(opts['wavemeter_server_ip'], opts['dist_sockets'][k]['port']))

    # init fiber switcher server
    sock_fiber = bind_socket(opts['fiber_server_ip'], opts['fiber_server_port'])

    return (wlm, dist_sockets, sock_fiber, fib)


#############################################################
# Run wavemeter server
#############################################################

def send_msg(connection, msg):

    len_msg = "{0:2d}".format(len(msg))
    
    # send the amount of data first
    connection.sendall(len_msg.encode())

    # send the data
    connection.sendall(msg)

    return


def run_dist_server(opts, wlm, q, sock):    

    # these servers distributes the frequencies upon request
    # there are multiple to avoid conflicts when accessing them from multiple computers

    # after receiving a request, the server sends two messages: one with the length of the response and one with the response

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()

        try:            
            request = connection.recv(7).decode()

            # Frequency of the wavemeter is requested and send back
            if request == 'request':
                freq = q.get()

                freq = ",".join(freq)
                
                msg = str(freq).encode()
                
                send_msg(connection, msg)

            # Calibration of the wavemeter is initiated
            elif request == 'reqch28':
                
                # receive tisa freq    
                wlm.SetExposure(100)
                switch_fiber_channel(opts, 2, wait_time = 0.25)

                freq_2 = wlm.frequency 
                freq_2 = "{0:10.6f}".format(freq_2)

                # receive comb freq   
                wlm.SetExposure(25)              
                switch_fiber_channel(opts, 8, wait_time = 0.25)

                freq_8 = wlm.frequency 
                freq_8 = "{0:10.6f}".format(freq_8)


                # send data back to Artiq
                freq_msg = "{0},{1}".format(freq_2, freq_8)

                msg = str(freq_msg).encode()

                send_msg(connection, msg)

                # back to channel 2
                switch_fiber_channel(opts, 2, wait_time = 0.1)


            # Calibration of the wavemeter is initiated
            elif request == 'henecal':
                
                # receive hene freq
                hene_freq = float(connection.recv(10).decode())
                chan_hene = 2

                switch_fiber_channel(opts, chan_hene, wait_time = 3)
    
                wlm.SetExposure(100)
                time.sleep(1)
                wlm.Calibration(hene_freq)

                # switch back to previous channel
                # wait since the wavemeter server will readout the hene frequency
                # ideally this readout would be stopped while calibrating
                switch_fiber_channel(opts, 0, wait_time = 3)

            # Calibration of the wavemeter is initiated
            elif request == 'daecali':
                
                # receive hene freq
                daenerys_freq       = float(connection.recv(10).decode())
                chan_green_daenerys = 7
                old_channel         = 3

                switch_fiber_channel(opts, chan_green_daenerys, wait_time = 3)
    
                wlm.SetExposure(10)
                time.sleep(1)
                wlm.Calibration(daenerys_freq)

                # switch back to previous channel
                # wait since the wavemeter server will readout the hene frequency
                # ideally this readout would be stopped while calibrating
                switch_fiber_channel(opts, old_channel, wait_time = 3)

            else:
                print('no more data from', client_address)
                break                       
            
        finally:
            # Clean up the connection
            connection.close()
        

################################
# Run Wavemeter Readout Server
################################

def run_wavemeter_readout_server(q, wlm, fib):

   # this server continuously reads out the current wavemeter frequency and adds it to the queue
   
   chans = [0]
   act_values = [0] * len(chans)
   
   try_trig = wlm.Trigger(3)
   
   new_freq = wlm.frequency
   
   while True:
       for l in range(len(chans)):
               wlm.Trigger(0)
               				
               try_trig = wlm.Trigger(3)
   
               # obtains the actual frequency value
               new_freq = wlm.frequency               
               
               act_values[l] = "{0:10.6f}".format(new_freq)
   
               for k in range(len(q)):
                   q[k].put(act_values)
   return


#############################
# Run Fiber Switcher Server
#############################

def run_fiber_switcher_server(opts, sock, fib, wlm):

    # switches the fiber switcher between channels 1-8
    # if chan = 0, then it switches to the previous channel

    previous_channel  = 1
    current_channel   = 1

    channel_exposures = opts['wavemeter_channel_exposures']
    

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()

        try:
            data = connection.recv(1)

            if data:
                chan = int(data.decode())

                if chan == 0:
                    # if chan == 0, then switch to previous channel
                    chan = previous_channel
                    
                    previous_channel = current_channel
                    current_channel = chan
                else:
                    previous_channel = current_channel
                    current_channel = chan

                # set exposure time
                wlm.SetExposure(channel_exposures[chan])

                # switch channel
                fib.setchan(chan)

            else:
                print('no more data from', client_address)
                break
            
        finally:
            # Clean up the connection
            connection.close()

    return




###############################################################################
# Main
###############################################################################

opts = {
    'fiber_switcher_com_port'   : 'COM8',
    'fiber_server_ip'           : '192.168.42.20',
    'fiber_server_port'         : 65000,
    'wavemeter_server_ip'       : '192.168.42.20',
    'dist_sockets' : [ # these are for the wavemeter distribution servers
        {
            'port' : 62500
        },
        {
            'port' : 62200
        }
        ],
    'wavemeter_channel_exposures' : {
            1 : 25,
            2 : 25,
            3 : 100, # Daenerys IR
            4 : 100, # HeNe channel
            5 : 450,
            6 : 450,
		    7 : 10,  # Daenerys Green
			8 : 25
    }
}






#########################
# Init server and sockets
#########################

(wlm, dist_sockets, sock_fiber, fib) = init_distribution_servers(opts)


# Run the wavemeter distribution servers in a thread

q_arr = []
for n in range(len(opts['dist_sockets'])):

    q_arr.append(queue.Queue())

    # distribution server 
    dist_server_thread = threading.Thread(target=run_dist_server, args=(opts, wlm, q_arr[n], dist_sockets[n],), daemon = True)
    dist_server_thread.start()


#current_channel = queue.Queue()

# Run the fiber switcher server in a thread

fiber_switcher_thread = threading.Thread(target=run_fiber_switcher_server, args=(opts, sock_fiber, fib, wlm,), daemon = True)
fiber_switcher_thread.start()


# Run the wavemeter readout server in a thread

readout_thread = threading.Thread(target=run_wavemeter_readout_server, args=(q_arr, wlm, fib,), daemon = True)
readout_thread.start()


while True:
    pass
	
	






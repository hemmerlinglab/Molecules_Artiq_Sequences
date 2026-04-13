import socket
import serial
import time
from simple_pid import PID
import threading
import queue
import numpy as np

from wlm import *

from arduino_control import *


#from line_profiler import profile



wlm = WavelengthMeter()

def z_new_get_frequencies(opts):
    try_trig = wlm.Trigger(3)
    new_freq = wlm.frequency
    output = "{0:10.6f}".format(new_freq)
    return float(output)

def get_frequencies(opts):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (opts['wavemeter_server_ip'], opts['wavemeter_server_port'])
    sock.connect(server_address)

    try:
        # Send data
        sock.sendall('request'.encode())

        data = sock.recv( int(sock.recv(2).decode()) )
        
        output = float(data.decode())

    finally:
        #print('closing socket')
        sock.close()

    return output


###################################################################
# Arduino Control Functions
###################################################################



#############################################################
# Switch Fiber Channel
#############################################################

def switch_fiber_channel(opts, channel, wait_time = None, manual_switch = False):

    # switch all PIDs to hold


    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (opts['fiber_server_ip'], opts['fiber_server_port'])
    print('Switching fiber channel on {0} port {1} to channel {2}'.format(server_address[0], server_address[1], channel))
    #sock.bind(server_address)

    sock.connect(server_address)

    sock.sendall(str(channel).encode())
    sock.close()

    #print(wait_time)

    if not wait_time == None:
        time.sleep(wait_time)

    # switch new PID to sample

    return 


#############################################################
# Server to receive new setpoint
#############################################################


def setup_setpoint_server(opts):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (opts['setpoint_server_ip'], opts['setpoint_server_port'])
    print('starting up set point server on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    return sock



def run_setpoint_server(q_arr, sock):
    while True:
        # Wait for a connection
        #print('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            # Receive the data in small chunks and retransmit it
            
            # data = 3,374.123456789,1,1234  = <wavemeter_channel>,<new set point>,<switch_to_channel>,<wait_time (ms)>

            data = connection.recv(22)
            
            #print(data)
            
            data = data.decode()
            data = data.split(',')

            data = {
                    "channel" : int(data[0]), 
                    "frequency" : float(data[1]), 
                    "switch_channel" : int(data[2]),
                    "wait_time" : int(data[3])
            }


            q_arr.put(data)

        finally:
            connection.close()




##################################################################
# PID
##################################################################


def init_pid(opts):

    act_values = {}

    pid_arr = {}

    init_setpoints = {}

    for k in opts['pids'].keys():

        curr_pid = opts['pids'][k]
    
        switch_fiber_channel(opts, curr_pid['wavemeter_channel'], wait_time = 1) 

        act_values[curr_pid['wavemeter_channel']] = get_frequencies(opts)
        
        setpoint = act_values[curr_pid['wavemeter_channel']]

        init_setpoints[curr_pid['wavemeter_channel']] = setpoint

        pid = PID(curr_pid['Kp'], curr_pid['Ki'], 0.0, setpoint, sample_time = 0.001, output_limits = [-10, 10])
    
        pid_arr[curr_pid['wavemeter_channel']] = pid

    return pid_arr, init_setpoints



def run_pid(q_arr, ser, pid_arr, current_channel, init_setpoints, opts):

    # q_arr : setpoints
    # pid_arr : pids

    act_values = {}
    setpoints = init_setpoints
    
    last_output = {}

    while True:        

        # check if there is a new setpoint
        try:
            var = q_arr.get(block = False)

            chan = var['channel']
            freq = var['frequency']
            switch_channel = var['switch_channel']
            wait_time = var['wait_time'] # 3300 = 3.3 seconds

            print(chan, freq, switch_channel, wait_time)

            if switch_channel == 1:
                
                # set current PID on hold
                pid_arr[current_channel].set_auto_mode(False) #, last_output = last_output[current_channel])

                # switch to new fiber channel
                switch_fiber_channel(opts, chan, wait_time = wait_time/1000.0)

                # switch current_channel to new channel
                current_channel = chan
                
                # activate PID of new channel
                pid_arr[current_channel].set_auto_mode(True, last_output = last_output[current_channel])

            # get specific setpoint of channel                
            if chan in setpoints.keys():

                 setpoints[chan] = freq
                
                 print()
                 print('New setpoint ... ' + str(setpoints))
                 print([pid_arr[c](act_values) for c in pid_arr.keys()])

    
        except queue.Empty:            
            #print('error2')
            pass
			        
		
        # loop over all channels
        for c in pid_arr.keys():

            #print(c)
    
            # run PID
            if (setpoints[c] > 0) and (pid_arr[c].auto_mode == True):


                pid_arr[c].setpoint = float(setpoints[c]) 
                
                #t1 = time.time()
                act_values = get_frequencies(opts) # slowest part
                #print("{0:.2f}".format(time.time() - t1))

                last_output[c] = pid_arr[c](act_values)
    
                # send control voltage to Arduino of laser
                send_arduino_control(ser[opts['pids'][c]['arduino_no']], last_output[c], opts['pids'][c]['DAC_chan'], max_output = opts['pids'][c]['DAC_max_output'])
   
                #print('{0:.2f} {1:.2f}'.format(act_values, last_output[c]))

            elif (setpoints[c] <= 0) and (pid_arr[c].auto_mode == True):
                last_output[c] = 0.0

    return


#################################################################
# Init servers
#################################################################

def init_all(opts):

    print('Init ...')
    ser = init_arduinos(com_ports = opts['arduino_com_ports'], init_output = True)
    
    sock = setup_setpoint_server(opts)
    
    print('Init PID ...')
    pid_arr, init_setpoints = init_pid(opts)
    
    # init fiber switcher
    switch_fiber_channel(opts, opts['fiber_switcher_init_channel'], wait_time = 0)
    
    # Queue allows for communicating between threads
    q_arr = queue.Queue()
    
    # start PID thread
    pid_thread = threading.Thread(target=run_pid, args=(q_arr, ser, pid_arr, opts['fiber_switcher_init_channel'], init_setpoints, opts), daemon = True)
    pid_thread.start()
    
    # start socket thread
    setpoint_thread = threading.Thread(target=run_setpoint_server, args=(q_arr, sock,), daemon = True)
    setpoint_thread.start()



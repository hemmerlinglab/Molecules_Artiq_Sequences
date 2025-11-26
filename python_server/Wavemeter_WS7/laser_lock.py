import socket
import serial
import time
from simple_pid import PID
import threading
import queue
import numpy as np

from arduino_control import *
from network_tools   import *


#####################################################################
# Query current wavemeter frequency
#####################################################################

def get_frequencies(opts):

    # connects to wavemeter distribution server and receives current frequency
    try:
        # send request
        sock = connect_and_send_socket(opts['wavemeter_server_ip'], opts['wavemeter_server_port'], 'request')

        # receive response
        len_msg = int(sock.recv(2).decode())

        data = sock.recv(len_msg)
        
        output = float(data.decode())

    finally:
        sock.close()

    return output


#############################################################
# Server to receive new setpoint
#############################################################

def run_setpoint_server(q_arr, sock):

    # the set point server waits for a connection from, e.g., Artiq, to receive a new setpoint
    while True:
        # Wait for a connection
        connection, client_address = sock.accept()

        try:
            # Receive the data and saves the setpoint in the queue q_arr
            
            # data = 3,374.123456789,1,1234  = <wavemeter_channel>,<new set point>,<switch_to_channel>,<wait_time (ms)>

            data = connection.recv(22)
            
            data = data.decode()
            data = data.split(',')

            data = {
                    "channel"        : int(data[0]), 
                    "frequency"      : float(data[1]), 
                    "switch_channel" : int(data[2]),
                    "wait_time"      : int(data[3])
            }


            q_arr.put(data)

        finally:
            connection.close()

    return


##################################################################
# PID
##################################################################

#################
# Init the PIDs
#################

def init_pid(opts):

    # Initialize the PIDs

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


#################
# Run the PIDs
#################

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

            chan           = var['channel']
            freq           = var['frequency']
            switch_channel = var['switch_channel']
            wait_time      = var['wait_time'] # 3300 = 3.3 seconds

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
            pass
			        
		
        # loop over all channels
        for c in pid_arr.keys():
    
            # run PID
            if (setpoints[c] > 0) and (pid_arr[c].auto_mode == True):

                pid_arr[c].setpoint = float(setpoints[c]) 
                act_values = get_frequencies(opts)

                #if c == 6:
                #    print("{0}, {1}, {2}".format(act_values, pid_arr[c].setpoint, control))

                last_output[c] = pid_arr[c](act_values)
    
                # send control voltage to Arduino of laser
                send_arduino_control(ser[opts['pids'][c]['arduino_no']], last_output[c], opts['pids'][c]['DAC_chan'], max_output = opts['pids'][c]['DAC_max_output'])
   

                #print("Output: {0} Act_values: {1} Set_point: {2}".format(last_output[c], act_values, setpoints[c]))
                #print(opts['pids'][c]['arduino_no'])
                #print(ser)
                #print(act_values)
                #print(last_output[c])

            #else:
            elif (setpoints[c] <= 0) and (pid_arr[c].auto_mode == True):
                last_output[c] = 0.0

            #print(new_setpoint)

    return


#################################################################
# Init servers/clients
#################################################################

def init_all(opts):

    print('Init ...')
    ser = init_arduinos(com_ports = opts['arduino_com_ports'], zero_init_output = True)
    
    sock_setpoint = bind_socket(opts['setpoint_server_ip'], opts['setpoint_server_port'])
    
    print('Init PID ...')
    pid_arr, init_setpoints = init_pid(opts)
    
    # init fiber switcher
    switch_fiber_channel(opts, opts['fiber_switcher_init_channel'], wait_time = 0)
    
    # Queue allows for communicating between threads
    q_arr = queue.Queue()
    
    # start PID thread
    pid_thread = threading.Thread(target=run_pid, args=(q_arr, ser, pid_arr, opts['fiber_switcher_init_channel'], init_setpoints, opts), daemon = True)
    pid_thread.start()
    
    # start setpoint servers
    setpoint_thread = threading.Thread(target=run_setpoint_server, args=(q_arr, sock_setpoint,), daemon = True)
    setpoint_thread.start()

    return



###################################
# Main
###################################

opts = {
        'arduino_com_ports' : {0 : 'COM4', 1 : 'COM7'},
        'wavemeter_server_ip' : '192.168.42.20',
        'wavemeter_server_port' : 62500,
        'setpoint_server_ip' : '192.168.42.20',
        'setpoint_server_port' : 63700,
        'fiber_server_ip' : '192.168.42.20',
        'fiber_server_port' : 65000,
        'pids' : {
            1 : {'laser' : 391, 'wavemeter_channel' : 1, 'Kp' : -10, 'Ki' : -5000, 'arduino_no' : 0, 'DAC_chan' : 1, 'DAC_max_output' : 4095.0},
            2 : {'laser' : 398, 'wavemeter_channel' : 2, 'Kp' : -5, 'Ki' : -5000, 'arduino_no' : 0, 'DAC_chan' : 2, 'DAC_max_output' : 4095.0},
			3 : {'laser' : 1046, 'wavemeter_channel' : 3, 'Kp' : -10, 'Ki' : -100000, 'arduino_no' : 1, 'DAC_chan' : 2, 'DAC_max_output' : 4095.0},
            8 : {'laser' : 1046, 'wavemeter_channel' : 8, 'Kp' : 10, 'Ki' : 100000, 'arduino_no' : 1, 'DAC_chan' : 1, 'DAC_max_output' : 4095.0}
            },
        'fiber_switcher_init_channel' : 2
        }
   


init_all(opts)


# keep deamons running
while True:
    pass





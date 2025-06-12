#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
import time
import matplotlib.pyplot as plt

from simple_pid import PID

from fft import FFT
from koheron import connect

import socket
import sys




#n_pts = driver.n_pts
N_PTS = 2048
FREQ_RANGE = 62.5/(N_PTS/2 - 1) * np.arange(1024)

# cut out only the 20 - 55 MHz range
IND_LIM_RANGE = np.where((FREQ_RANGE > 10) & (FREQ_RANGE < 40))[0]




def conv2bit(V):

    # Converts the +/- 1V of the red pitaya outputs to a 14-bit (15th bit is used for the sign)

    if V >= 0:
        my_bits = int( (2**15 - 1) * V )
    else:
        my_bits = int( 2**16 - 2**15 * abs(V) )

    return my_bits


def RP():
    # initializes RP

    host = os.getenv('HOST', '192.168.42.53')
    client = connect(host, 'fft', restart=False)
    driver = FFT(client)

    driver.set_input_channel(1)
    #driver.set_output(conv2bit(0))

    return driver



################################################################################

def get_curr_frequency(driver):

    # gets the current frequency peak from the FPGA FFT and extracts the frequency value


    psd = driver.read_psd()

    psd = psd[IND_LIM_RANGE]

    ind = np.where(psd == np.max(psd))[0][0]
    
    curr_freq = FREQ_RANGE[IND_LIM_RANGE][ind]


    # apply empirical correction
    #curr_freq -= (-0.003 + -0.000425)*( (curr_freq-3) % (21-3) ) - 0.03 + (0.06)/62.5 * curr_freq

    return (curr_freq, np.log10(psd[ind]))




################################################################################

def get_wavemeter_readings():

    # reads out laser frequencies from wavemeter

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.42.20', 62200)

    sock.connect(server_address)

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
    freqs = float(data.decode())

    #print('Getting laser frequencies ... {0:.6f} THz'.format(freqs))
    
    return freqs


################################################################################

def lock_laser(rp, pid, setpoint, no_of_steps = None, sign = +1, last_output = 0.0):

    print()
    
    pid_out = []
    act     = []

    # set pid setpoint
    pid.setpoint = setpoint

    pid.Kp = sign * pid.Kp
    pid.Ki = sign * pid.Ki
    pid.Kd = sign * pid.Kd

    #pid.set_auto_mode(True, last_output = last_output)

    wlm_1 = get_wavemeter_readings()
    
    if no_of_steps == None:
        total_steps = 1e10
    else:
        total_steps = no_of_steps

    k = 0
    
    pid.auto_mode = True
    
    while k < total_steps:
    
        # read out power spectral density from RP
        psd = rp.read_psd()

        psd = psd[IND_LIM_RANGE]

        ind = np.where(psd == np.max(psd))[0][0]
    
        curr_freq = FREQ_RANGE[IND_LIM_RANGE][ind]

        lvl = np.log10(psd[ind])



        output = pid(curr_freq)
    
        pid_out.append(output)
        act.append(curr_freq)


        rp.set_output(conv2bit(output))


        print("set: {0:.2f} MHz; act: {1:.2f} MHz; lvl: {3:.2f}; out: {2:.2f}".format(pid.setpoint, curr_freq, output, lvl), end = '\r')

        k += 1
    
        #if k == 10:
        #    print(get_wavemeter_readings())

    wlm_2 = get_wavemeter_readings()

    #pid.auto_mode = False
    
    print()


    return (wlm_1, wlm_2, pid_out, act)


################################################################################

def dry_run(rp):
    
    pid_out = []
    act     = []

    for k in range(50):

        # read out power spectral density from RP
        psd = rp.read_psd()

        psd = psd[IND_LIM_RANGE]

        ind = np.where(psd == np.max(psd))[0][0]
    
        curr_freq = FREQ_RANGE[IND_LIM_RANGE][ind]

        lvl = np.log10(psd[ind])

        pid_out.append(0.0)

        act.append(curr_freq)


    return (pid_out, act)



####################################################
# Main
####################################################

rp  = RP()


factor = 1.0 

kp = 1e-2
ki = 5e-1
kd = 0.0

sign = -1

no_of_steps = 20000



pid = PID(kp, ki, kd)

pid.auto_mode = False

pid.sample_time = 0.1e-3

pid.output_limits = (-1, 1)



freq = 23


print('Setting output of RP to 0.0V')
rp.set_output(conv2bit(0.0))

(pid_dry1, act_dry1) = dry_run(rp)

(wb_1, wa_1, pid_out1, act1) = lock_laser(rp, pid, freq, no_of_steps = no_of_steps, sign = sign)

print('before: {0:.6f} after: {1:.6f}'.format(wb_1, wa_1))

pid.auto_mode = False

(pid_dry2, act_dry2) = dry_run(rp)


print('Setting output of RP to 0.0V')
rp.set_output(conv2bit(0.0))


#################################################
# Analysis
#################################################

pid_out = []
pid_out.extend(pid_dry1)
pid_out.extend(pid_out1)
pid_out.extend(pid_dry2)

acts = []
acts.extend(act_dry1)
acts.extend(act1)
acts.extend(act_dry2)

rp.set_output(conv2bit(0))


plt.figure()
plt.subplot(2,1,1)
plt.plot(pid_out, label = 'pid out')

plt.legend()

plt.subplot(2,1,2)
plt.plot(acts, label = 'act freq')
plt.ylim(20, 30)

plt.legend()

plt.show()





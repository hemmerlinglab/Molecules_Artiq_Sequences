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
IND_LIM_RANGE = np.where((FREQ_RANGE > 10) & (FREQ_RANGE < 60))[0]




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



def get_curr_frequency(driver):

    # gets the current frequency peak from the FPGA FFT and extracts the frequency value


    psd = driver.read_psd()

    psd = psd[IND_LIM_RANGE]

    ind = np.where(psd == np.max(psd))[0][0]

    #plt.plot(FREQ_RANGE, np.log10(psd))
    #plt.plot(FREQ_RANGE[IND_LIM_RANGE], np.log10(psd))
    #plt.show()

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

    pid.set_auto_mode(True, last_output = last_output)

    wlm_1 = get_wavemeter_readings()
    
    if no_of_steps == None:
        total_steps = 1e10
    else:
        total_steps = no_of_steps

    k = 0
    while k < total_steps:
    
        (curr_freq, lvl) = get_curr_frequency(rp)
    
        if (curr_freq > 5) and (curr_freq < 60) and (lvl > -20.0):
            #pid.auto_mode = True
            output = pid(curr_freq)
    
            pid_out.append(output)
            act.append(curr_freq)

        else:
            pid.auto_mode = False
            output = 0
    
        rp.set_output(conv2bit(output))
    
        print("set: {0:.2f} MHz; act: {1:.2f} MHz; lvl: {3:.2f}; out: {2:.2f}".format(pid.setpoint, curr_freq, output, lvl), end = '\r')

        k += 1

    pid.auto_mode = False
    
    wlm_2 = get_wavemeter_readings()

    print()


    return (wlm_1, wlm_2, pid_out, act)





####################################################
# Main
####################################################

factor = 1.0 # since we measure in the green

kp =  1e-2
ki = 30e-2
kd = 0.0

sign = +1

no_of_steps = 1000

rp  = RP()


pid = PID(kp, ki, kd)


pid.sample_time = 0.1e-3

pid.output_limits = (-1, 1)

pid.auto_mode = True


two_freq = [23, 42]


(wb_1, wa_1, pid_out1, act1) = lock_laser(rp, pid, two_freq[0], no_of_steps = no_of_steps, sign = sign)

print('before: {0:.6f} after: {1:.6f}'.format(wb_1, wa_1))

(wb_2, wa_2, pid_out2, act2) = lock_laser(rp, pid, two_freq[1], no_of_steps = no_of_steps, sign = sign, last_output = pid_out1[-1])

print('before: {0:.6f} after: {1:.6f}'.format(wb_2, wa_2))


beat_node_shift = two_freq[1] - two_freq[0]
wavemeter_shift = (wa_2 - wa_1)*1e12/1e6



print()
print('Frequency lock:        {0} -> {1} MHz, diff: {2} MHz'.format(two_freq[0], two_freq[1], beat_node_shift))
print('Wavemeter reading:     {0:.6f} -> {1:.6f} THz = diff: {2:.0f} MHz'.format(wa_1, wa_2, wavemeter_shift))
print('Wavemeter reading * 2: {0:.6f} -> {1:.6f} THz = diff: {2:.0f} MHz'.format(wa_1 * 2, wa_2 * 2, 2*wavemeter_shift))

print()
print('If both values are positive, that means the beat node is on the right (higher frequency) side of a comb tooth.')
print()


vrep = 200e6


# wavemeter and beat node move in the same direction
# beat node is at the higher frequency side of a comb tooth
if (np.sign(wavemeter_shift) == np.sign(beat_node_shift)):

    n_tooth = np.floor( factor * wa_2*1e12 / vrep )

    true_frequency = n_tooth * vrep + two_freq[1] * 1e6

else:

    n_tooth = np.ceil( factor * wa_2*1e12 / vrep )

    true_frequency = n_tooth * vrep - two_freq[1] * 1e6




print('Comb tooth: {0:.0f}'.format(n_tooth))

print()
print('True frequency locked @ {2:.0f} MHz\n    (IR):    {0:.6f} THz\n    (Green): {1:.6f} THz'.format(true_frequency/1e12, true_frequency/1e12 * 2.0, two_freq[1]))

print()
print('Wavemeter status: \n Current value: (IR):  {0:.6f} THz\n True value:    (IR):  {1:.6f} THz\n Difference: {2:.0f} MHz'.format(wa_2, true_frequency/1e12, (true_frequency/1e12 - wa_2)*1e12/1e6))




# keep laser locked

(w1, w2, pid_out3, act3) = lock_laser(rp, pid, two_freq[1], sign = sign, last_output = pid_out2[-1])





#################################################
# Analysis
#################################################

pid_out = []
pid_out.extend(pid_out1)
pid_out.extend(pid_out2)

acts = []
acts.extend(act1)
acts.extend(act2)

rp.set_output(conv2bit(0))


plt.figure()
plt.subplot(2,1,1)
plt.plot(pid_out, label = 'pid out')

plt.legend()

plt.subplot(2,1,2)
plt.plot(acts, label = 'act freq')
plt.ylim(20, 50)

plt.legend()

plt.show()





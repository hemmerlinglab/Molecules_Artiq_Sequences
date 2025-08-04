import os
import sys
import time
import socket
import numpy as np

from base_sequences import set_zotino_voltage


# Instrument imports
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server")
sys.path.append("/home/molecules/software/Molecules_Artiq_Sequences/python_server/Windfreak")

from rigol               import Rigol_RSA3030, Rigol_DSG821
from frequency_comb      import DFC
from microwave_windfreak import Microwave



#######################################################################################################

def load_instruments(self):
 
    # Load all instruments specified when calling the base_build
    for instr in self.which_instruments:

        if instr == 'EOM':
            self.EOM_function_generator = Rigol_DSG821()

        if instr == 'frequency_comb':
            self.frequency_comb         = DFC()

        if instr == 'microwave':
            self.microwave              = Microwave()

        if instr == 'spectrum_analyzer':
            self.spectrum_analyzer      = Rigol_RSA3030()

            self.spectrum_analyzer.set_freq([2e6, 205e6])

    return


#######################################################################################################

def prepare_initial_instruments(self):

    # set initial helium flow
    set_helium_flow(self.he_flow, wait_time = self.he_flow_wait)

    # set voltage on plate
    set_zotino_voltage(self, 0, self.plate_voltage)
   
    #####################################
    # Set microwave power
    #####################################
    
    if 'microwave' in self.which_instruments:
        
        self.microwave.power(self.microwave_power)
        self.microwave.freq(self.microwave_frequency * 1e6)
    
    #####################################
    # Set initial laser frequencies
    #####################################
    
    # init scanning laser
    if self.scanning_laser   == 'Daenerys':
        hlp_frequency_offset = self.offset_laser_Daenerys
    elif self.scanning_laser == 'Hodor':
        hlp_frequency_offset = self.offset_laser_Hodor
    elif self.scanning_laser == 'Davos':
        hlp_frequency_offset = self.offset_laser_Davos

    set_single_laser(self.scanning_laser, hlp_frequency_offset, do_switch = True, wait_time = self.relock_wait_time)

    # pause to wait till laser settles
    time.sleep(1)

    return


#######################################################################################################

def close_instruments(self):
 
    # Disconnect instruments
    # Load all instruments specified when calling the base_build
    for instr in self.which_instruments:
        if instr == 'EOM':
            self.EOM_function_generator.close()

        if instr == 'frequency_comb':
            self.frequency_comb.close()

        if instr == 'microwave':
            self.microwave.off()
            self.microwave.close()

        if instr == 'spectrum_analyzer':
            self.spectrum_analyzer.close()

    return



#######################################################################################################

def reset_instruments(self):

    #####################################
    # Reset laser frequencies
    #####################################
    
    # init scanning laser
    if self.scanning_laser   == 'Daenerys':
        hlp_frequency_offset = self.offset_laser_Daenerys
    elif self.scanning_laser == 'Hodor':
        hlp_frequency_offset = self.offset_laser_Hodor
    elif self.scanning_laser == 'Davos':
        hlp_frequency_offset = self.offset_laser_Davos

    # set laser back to initial point
    set_single_laser(self.scanning_laser, hlp_frequency_offset, wait_time = self.lock_wait_time)

    # switch off Helium flow
    set_helium_flow(0.0, wait_time = 0.0)

    # set plate voltage for zero again
    set_zotino_voltage(self, 0, 0)

    if 'microwave' in self.which_instruments:
        # switch off microwave
        self.microwave.off()

    return


#######################################################################################################

def set_helium_flow(flow, wait_time = 10.0):

    # Sets Helium flow
    
    # flow in sccm

    print('Changing flow to ... {0:.3f} sccm'.format(flow))

    path = '/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions/mfc_exec' 

    os.system('{0} 192.168.42.99 -s {1:.3f}  >/dev/null 2>&1'.format(path, flow / 5.0))

    # wait until flow has settled
    print('Waiting for flow to settle ... {0} s'.format(wait_time))
    time.sleep(wait_time)

    return


#######################################################################################################

def move_yag_mirror(xpos, ypos, wait_time = None):

    # Moves Yag Mirror

    # init connection to python server to send commands to move mirrors
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.42.20', 62000)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    message = "{0:5.3f}/{1:5.3f}".format(xpos, ypos)
    print('Moving mirrors ... ' + message)
    
    sock.sendall(message.encode())

    if not wait_time == None:
        time.sleep(wait_time)

    sock.close()

    return


#######################################################################################################

def get_wavemeter_readings():

    # reads out laser frequencies from wavemeter

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.42.20', 62200)

    sock.connect(server_address)

    ## 'request' gets only one frequency
    #try:    
    #    # Request data
    #    message = 'request'
    #    #print('sending "%s"' % message)
    #    sock.sendall(message.encode())

    #    len_msg = int(sock.recv(2).decode())

    #    data = sock.recv(len_msg)

    print('asd')
    # 'request' gets only one frequency
    try:    
        # Request data
        message = 'reqch28'
        #print('sending "%s"' % message)
        sock.sendall(message.encode())

        len_msg = int(sock.recv(2).decode())

        data = sock.recv(len_msg)

    finally:
        sock.close()

    print('done')

    # return a list of freqs
    # currently only one frequency is returned
    freqs = data.decode().split(',')

    freqs = [ float(x) for x in freqs ]
    #print(freqs)

    #print('Getting laser frequencies ... {0:.6f} THz'.format(freqs))
    
    return freqs


#######################################################################################################

def set_single_laser(which_laser, frequency, do_switch = False, wait_time = None):

    if which_laser == 'Davos':
        channel = 1
    elif which_laser == 'Hodor':
        channel = 2
    elif which_laser == 'Daenerys':
        channel = 3
    else:
        print('Error: No laser to set or scan')
        asd

    if do_switch:
        switch = 1
    else:
        switch = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.settimeout(1)

    server_address = ('192.168.42.20', 63700)

    print('Sending new setpoint for {1}: {0:.6f}'.format(frequency, which_laser))
    
    try:

        sock.connect(server_address)

        message = "{0:1d},{1:.9f},{2:1d},{3:3d}".format(int(channel), float(frequency), int(switch), int(wait_time))

        sock.sendall(message.encode())

        sock.close()

        if not wait_time == None:
            time.sleep(2*wait_time/1000.0)

    except socket.timeout:
        print('Timeout sending setpoint')

    return




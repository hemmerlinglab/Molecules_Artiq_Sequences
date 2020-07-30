import os
import socket
import sys
import numpy as np
import time

def calibrate(channel, freq):
    # calibrate wavemeter
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.42.20', 63800)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)
    
    message = '1,' + str(channel) + ',' + "{0:10.6f}".format(freq)
    sock.sendall(message.encode())
    sock.close()
   
    # replace with feedback of wavemeter
    time.sleep(10)


def init_freq(channel, freq):
    # calibrate wavemeter
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.42.20', 63800)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)
    
    message = '0,' + str(channel) + ',' + "{0:10.6f}".format(freq)
    sock.sendall(message.encode())
    sock.close()




if len(sys.argv) == 2:
    if sys.argv[1] == 'init':

        channel = 1

        hene_freq = 473.612512e12
        laser_freq = 382.110450e12

        calibrate(channel, hene_freq/1e12)
        
        init_freq(channel, laser_freq/1e12)


    if sys.argv[1] == 'run':
        
        # loop over calibration frequencies

        channel = 1

        hene_freq = 473.612512e12
        
        calib_freq_arr = np.linspace(hene_freq - 10e6, hene_freq + 10e6, 2)
        
        #calib_freq_arr = [hene_freq]
        
        for n in range(len(calib_freq_arr)):
        
            calib_freq = calib_freq_arr[n]
        
            calibrate(channel, calib_freq/1e12)
        
            # wavemeter_offset (MHz)
            #wavemeter_offset = (calib_freq - hene_freq)/1e6
            
            wavemeter_offset = 0.8 * (calib_freq - hene_freq)/1e6 - 18.0
        
            ext = str(n) + '_35'
            wm_str = "{0:.1f}".format(wavemeter_offset)
            hene_calib_str = "{0:10.6f}".format(calib_freq/1e12)
            
            freq_offset_str = "{0:10.6f}".format(382.115147)
        
            # scan over AlCl R11 - 35
            os.system('artiq_run -q Molecules/Scan_Single_Laser_Socket.py extension=' + ext + ' + scan_count=2 setpoint_count=10 setpoint_min=-200 setpoint_max=200 setpoint_offset=' + freq_offset_str  + '  wavemeter_offset=' + wm_str + ' hene_calibration=' + hene_calib_str)

            ext = str(n) + '_37'

            freq_offset_str = "{0:10.6f}".format(382.117097)
        
            # scan over AlCl R11 - 37
            os.system('artiq_run -q Molecules/Scan_Single_Laser_Socket.py extension=' + ext + ' + scan_count=2 setpoint_count=10 setpoint_min=-200 setpoint_max=200 setpoint_offset=' + freq_offset_str  + '  wavemeter_offset=' + wm_str + ' hene_calibration=' + hene_calib_str)
        
        
            # scan over rubidium lines
            # os.system('artiq_run -q Calibrations/scan_reference_cell_socket.py scan_count=1 setpoint_offset=377.107 wavemeter_offset=' + wm_str + ' hene_calibration=' + hene_calib_str + ' extension=' + ext)
        
        # going back to regular Hene value
        calibrate(hene_freq/1e12)





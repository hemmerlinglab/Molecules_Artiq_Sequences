import os
import socket
import sys
import numpy as np
import time

def calibrate(freq):
    # calibrate wavemeter
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.42.20', 63800)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)
    
    message = '1,2,' + "{0:10.6f}".format(freq)
    sock.sendall(message.encode())
    sock.close()
   
    # replace with feedback of wavemeter
    time.sleep(10)


if len(sys.argv) == 2:
    if sys.argv[1] == 'run':

        # loop over calibration frequencies
        
        hene_freq = 473.612512e12
        
        calib_freq_arr = np.linspace(hene_freq - 300e6, hene_freq + 300e6, 30)
        
        #calib_freq_arr = [hene_freq]
        
        for n in range(len(calib_freq_arr)):
        
            calib_freq = calib_freq_arr[n]
        
            calibrate(calib_freq/1e12)
        
            # wavemeter_offset (MHz)
            #wavemeter_offset = (calib_freq - hene_freq)/1e6
            
            wavemeter_offset = 0.8 * (calib_freq - hene_freq)/1e6 - 18.0
        
            ext = str(n)
            wm_str = "{0:.1f}".format(wavemeter_offset)
            hene_calib_str = "{0:10.6f}".format(calib_freq/1e12)
        
            # scan over AlCl
            os.system('artiq_run -q Molecules/Scan_Single_Laser_Socket.py wavemeter_offset=' + wm_str + ' hene_calibration=' + hene_calib_str)
        
            # scan over rubidium lines
            # os.system('artiq_run -q Calibrations/scan_reference_cell_socket.py scan_count=1 setpoint_offset=377.107 wavemeter_offset=' + wm_str + ' hene_calibration=' + hene_calib_str + ' extension=' + ext)
        
        
        
        # going back to regular Hene value
        calibrate(hene_freq/1e12)





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
    time.sleep(20)



# loop over calibration frequencies

hene_freq = 473.612512e12

calib_freq_arr = np.linspace(hene_freq - 50e6, hene_freq + 50e6, 2)

for n in range(len(calib_freq_arr)):

    calib_freq = calib_freq_arr[n]

    calibrate(calib_freq/1e12)

    wavemeter_offset = -(hene_freq - calib_freq)/1e6

    ext = str(n)
    wm_str = "{0:.1f}".format(wavemeter_offset)
    hene_calib_str = "{0:10.6f}".format(calib_freq/1e12)

    #print(wm_str)
     
    # scan over rubidium lines
    os.system('artiq_run -q Calibrations/scan_reference_cell_socket.py scan_count=1 setpoint_offset=377.107 wavemeter_offset=' + wm_str + ' hene_calibration=' + hene_calib_str + ' extension=' + ext)







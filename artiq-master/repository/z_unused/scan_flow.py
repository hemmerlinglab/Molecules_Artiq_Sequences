import os
import socket
import sys
import numpy as np
import time





def run_seq(ext, laser_freq, wavemeter_offset, calib_freq):

    wm_str = "{0:.1f}".format(wavemeter_offset)
    hene_calib_str = "{0:10.6f}".format(calib_freq/1e12)
            
    freq_offset_str = "{0:10.6f}".format(laser_freq/1e12)
 
    os.system('artiq_run -q Molecules/Scan_Single_Laser_Socket.py extension=' + ext + ' scan_count=10 setpoint_count=20 setpoint_min=-250 setpoint_max=250 which_scanning_laser=1 offset_laser1=' + freq_offset_str  + '  wavemeter_offset=' + wm_str + ' hene_calibration=' + hene_calib_str + ' yag_check=True blue_check=True')




def set_flow(flow):

    # flow in sccm

    os.system('mfc 192.168.42.99 -s ' + "{0:f}".format(flow / 5.0))

    return



if len(sys.argv) == 2:

    #laser_freq_Q00 = 382.110400e12
    #laser_freq_R00 = 382.115147e12
    laser_freq_R11 = 382.120037e12
    hene_freq = 473.612512e12
    
    channel = 1

    if sys.argv[1] == 'init':

        laser_freq = laser_freq_R11

        calibrate(channel, hene_freq/1e12)
        init_freq(channel, laser_freq/1e12)

    if sys.argv[1] == 'run':
        
        # loop over calibration frequencies

        calib_freq_arr = np.linspace(hene_freq - 500e6, hene_freq + 500e6, 10)
        
        #calib_freq_arr = [hene_freq]
        
        for n in range(len(calib_freq_arr)):
        
            calib_freq = calib_freq_arr[n]
        
            calibrate(channel, calib_freq/1e12)
        
            # wavemeter_offset (MHz)
            wavemeter_offset = 0.8 * (calib_freq - hene_freq)/1e6 - 18.0
        
            print('Running scan over R11 - 35')
            laser_freq = laser_freq_R11

            run_seq('100' + str(n), laser_freq, wavemeter_offset, calib_freq)
            
            #time.sleep(2)
            
            #print('Running scan over R00 - 37')
            #laser_freq = 382.117097e12
            
            #run_seq('200' + str(n), laser_freq, wavemeter_offset, calib_freq)
                   
            # scan over rubidium lines
            # os.system('artiq_run -q Calibrations/scan_reference_cell_socket.py scan_count=1 setpoint_offset=377.107 wavemeter_offset=' + wm_str + ' hene_calibration=' + hene_calib_str + ' extension=' + ext)
        
        # going back to regular Hene value





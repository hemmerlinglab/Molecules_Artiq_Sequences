import numpy as np
import os.path
import datetime
import shutil
from configparser import ConfigParser
import socket
import socket
import os
import time
#from keysight import Keysight

def set_helium_flow(flow, wait_time = 10.0):

    # flow in sccm

    print('Changing flow to ... {0:.3f} sccm'.format(flow))

    path = '/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/repository/helper_functions/mfc_exec' 

    os.system('{0} 192.168.42.99 -s {1:.3f}  >/dev/null 2>&1'.format(path, flow / 5.0))

    # wait until flow has settled
    print('Waiting for flow to settle ... {0} s'.format(wait_time))
    time.sleep(wait_time)

    return


def move_yag_mirror(xpos, ypos, wait_time = None):

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

def get_single_laser_frequencies():

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

    print('Getting laser frequencies ... {0:.6f} THz'.format(freqs))
    
    return freqs



    


#def get_keysight_trace():
#
#    # Extracts single trace from spectrum analyzer
#
#    spec = Keysight()
#
#    low_freq = 1e6 
#    high_freq = 211e6
#
#    span_freq = high_freq - low_freq
#    cnt_freq = (high_freq + low_freq)/2.0
#
#    spec.set_center_freq(cnt_freq)
#    spec.set_span(span_freq)
#
#    spec.set_sweep()
#
#    (m1, m2, m3) = spec.do_peak_search()
#    
#    peaks = [m1, m2, m3]
#
#    try:
#        d = spec.get_trace()
#    except:
#        d = []
#    spec.close()
#    
#    return (d, peaks)


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

    server_address = ('192.168.42.20', 63700)

    print('Sending new setpoint for {1}: {0:.6f}'.format(frequency, which_laser))
    sock.connect(server_address)

    message = "{0:1d},{1:.9f},{2:1d},{3:3d}".format(int(channel), float(frequency), int(switch), int(wait_time))

    sock.sendall(message.encode())

    sock.close()

    if not wait_time == None:
        time.sleep(2*wait_time/1000.0)

    return



def get_basefilename(self, extension = ''):
    my_timestamp = datetime.datetime.today()
    
    self.today = datetime.datetime.today()
    self.today = self.today.strftime('%Y%m%d')

    self.datafolder = '/home/molecules/software/data/'
    self.setpoint_filename_laser1 = '/home/molecules/skynet/Logs/setpoint.txt'
    self.setpoint_filename_laser2 = '/home/molecules/skynet/Logs/setpoint2.txt'
 
    basefolder = str(self.today) # 20190618
    # create new folder if doesn't exist yet
    if not os.path.exists(self.datafolder + basefolder):
        os.makedirs(self.datafolder + basefolder)

    self.scan_timestamp = str(my_timestamp.strftime('%Y%m%d_%H%M%S'))

    self.basefilename = self.datafolder + basefolder + '/' + self.scan_timestamp # 20190618_105557

    # add optional extension
    if not extension is '':
        self.basefilename += '_' + str(extension)

        self.scan_timestamp += '_' + str(extension)


def save_all_data(self):
    # loops over data_to_save and saves all data sets in the array self.data_to_save
    for hlp in self.data_to_save:
        # transform into numpy arrays
        arr = np.array(self.get_dataset(hlp['var']))
       
        # Write Data to Files
        f_hlp = open(self.basefilename + '_' + hlp['var'],'w')
        np.savetxt(f_hlp, arr, delimiter=",")
        f_hlp.close()


def add_scan_to_list(self):
    # Write Data to Files
    f_hlp = open(self.datafolder + '/' + self.today + '/' + 'scan_list_' + self.today, 'a')
    f_hlp.write(self.scan_timestamp + '\n')
    f_hlp.close()


def save_config(basefilename, var_dict):

        # save run configuration
        # creates and overwrites config file
        # var_dict is an array of dictionaries
        # var_dict[0] = {
        #    'par': <parameter name>,
        #    'val': <parameter value>,
        #    'unit': <parameter unit>, (optional)
        #    'cmt': <parameter comment> (optional)
        #    }

        optional_parameters = ['unit', 'cmt']        
        conf_filename = basefilename + '_conf'

        # use ConfigParser to save config options
        config = ConfigParser()

        # create config file
        conf_file = open(conf_filename, 'w')
        print('Config file written.')

        # add scan name to config file
        config['Scan'] = {'filename' : basefilename}

        # toggle through dictionary and add the config categories
        for d in var_dict:
            config[d['par']] = {'val' : d['val']}

            for opt in optional_parameters:
                if opt in d.keys():
                    config[d['par']].update({opt : d[opt]})

        config.write(conf_file)

        # save also the sequence file 
        #print(config['sequence_file']['val'])
        #print(basefilename + '_sequence')
        shutil.copyfile(config['sequence_file']['val'], basefilename + '_sequence')
        
        conf_file.close()
        



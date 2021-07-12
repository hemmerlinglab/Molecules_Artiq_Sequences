import numpy as np
import os.path
import datetime
import shutil
from configparser import ConfigParser
import socket
import socket


def set_laser_frequency(channel, frequency):
    # channel = 1,2,...
    # frequency = 377.124354 

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.42.20', 63800)
    #print('connecting to %s port %s' % server_address)
    sock.connect(server_address)
    message = "{0},{1},{2:10.6f}".format(0,np.int(channel),frequency)
    sock.sendall(message.encode())

    sock.close()

    return
 

def get_laser_frequencies():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #server_address = ('localhost', 10000)
    # server_address = ('192.168.42.20', 63800)
    server_address = ('192.168.42.20', 62500)
    #print('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:
    
        # Send data
        message = 'request'
        #print('sending "%s"' % message)
        sock.sendall(message.encode())

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
    
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            #print('received "%s"' % data)

    finally:
        #print('closing socket')
        sock.close()

    # return a list of freqs
    # currently only one frequency is returned
    freqs = [np.float(data.decode())]

    return freqs

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
        



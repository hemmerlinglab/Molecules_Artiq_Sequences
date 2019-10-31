import numpy as np
import os.path
import datetime
from configparser import ConfigParser

def get_basefilename():
    my_today = datetime.datetime.today()
 
    datafolder = '/home/molecules/software/data/'
    setpoint_filename = '/home/molecules/skynet/Logs/setpoint.txt'
 
    basefolder = str(my_today.strftime('%Y%m%d')) # 20190618
    # create new folder if doesn't exist yet
    if not os.path.exists(datafolder + basefolder):
        os.makedirs(datafolder + basefolder)
 
    return datafolder + basefolder + '/' + str(my_today.strftime('%Y%m%d_%H%M%S')) # 20190618_105557


def save_all_data(self):
    # loops over data_to_save and saves all data sets in the array self.data_to_save
    for hlp in self.data_to_save:
        # transform into numpy arrays
        arr = np.array(self.get_dataset(hlp['var']))
       
        # Write Data to Files
        f_hlp = open(self.basefilename + '_' + hlp['var'],'w')
        np.savetxt(f_hlp, arr, delimiter=",")
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

        #if os.path.isfile(conf_filename):
        #    # append to config file
        #    conf_file = open(conf_filename, 'a')
        #else:
        #    # create config file
        #    conf_file = open(conf_filename, 'w')
        #    print('Config File Written')

        #    # add scan name to config file
        #    config['Scan'] = {'filename' : basefilename}
        
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


               
        conf_file.close()
        



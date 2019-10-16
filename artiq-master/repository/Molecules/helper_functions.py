import numpy as np
import os.path
from configparser import ConfigParser

def save_all_data(basefilename, var_dict):

    # var_dict = 1D array of dictionaries
    # var_dict[0] = {'var' : <1D list/array variable to save>, 'name' : <filename to save>}

    for hlp in var_dict:
        # transform into numpy arrays         
        arr = np.array(hlp['var'])
        
        # Write Data to Files
        f_hlp = open(basefilename + '_' + hlp['name'],'w')
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
        print('Config File Written')

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
        



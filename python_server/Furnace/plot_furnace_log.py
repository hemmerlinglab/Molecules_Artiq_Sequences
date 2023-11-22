import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os



def get_ccd_data(main_path):

    my_times = []
    d = []

    y = range(395, 500)
    y = range(395, 1900)

    for k in y:

        filename = 'test00000{0:04d}.csv'.format(k)

        hlp = np.genfromtxt(main_path + filename, delimiter = ';', skip_header = 49, skip_footer = 1)

        # get spectrum
        d.append(hlp[:, 1])
            
        # get time stamp
        f = open(main_path + filename, 'r')
        f.readline()
        f.readline()
        
        my_date = f.readline().split(';')[1].strip()
        
        f.readline()
        my_t    = f.readline().split(';')[1][0:6]

        f.close()

        timestamp = datetime.strptime(my_date + '-' + my_t, "%Y%m%d-%H%M%S")
        
        my_times.append(timestamp)

    x = hlp[:, 0]


    return (x, y, np.array(my_times, dtype = np.datetime64), np.array(d))


def get_furnace_data(main_path):

    f = open(main_path + 'furnace_log.csv')
    
    lines = f.readlines()

    d = { 'times' : [], 'data' : [] }

    for k in range(len(lines)):
    
        hlp = lines[k].split(',')
    
        timestamp = datetime.strptime(hlp[0], "%Y/%m/%d-%H:%M:%S")
        Tset = float(hlp[2])
        Tact = float(hlp[4])
        out = float(hlp[6])

        d['times'].append(timestamp)
        d['data'].append([Tset, Tact, out])

    d['times'] = np.array(d['times'], dtype = np.datetime64)
    d['data'] = np.array(d['data'])

    return d


def find_temp_at_time(d_f, ccd_times):

    temp_arr = []
    for k in range(len(ccd_times)):

        t0 = ccd_times[k]

        # time stamps furnace
        ind = np.where( np.abs(t0 - d_f['times']) < timedelta(seconds = 10) )

        temp_arr.append(d_f['data'][ind[0][0], 1])

    return np.array(temp_arr)



############################################################

# Potassium 769.9 nm

main_path = '/Users/boerge/Software/offline_furnace/'


d_f = get_furnace_data(main_path)

(x, y, ccd_times, d) = get_ccd_data(main_path)

temp_arr = find_temp_at_time(d_f, ccd_times)



plt.figure()

plt.subplot(2,1,1)

plt.plot(d_f['times'], d_f['data'][:, 1])

plt.subplot(2,1,2)

plt.pcolor(y, x, np.transpose(d))


plt.xlabel('Wavelength (nm)')
plt.ylabel('Spectrum Index')



plt.figure()

for k in [3, 10, 20, 500]:

    plt.plot(x, d[k], label = 'Temp {0} C'.format(temp_arr[k]))


plt.show()






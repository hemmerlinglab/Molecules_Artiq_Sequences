import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter
import os
import pickle


def get_single_file(filename):

    hlp = np.genfromtxt(filename, delimiter = ';', skip_header = 49, skip_footer = 1)
        
    # get time stamp
    f = open(filename, 'r')
    f.readline()
    f.readline()
    
    my_date = f.readline().split(';')[1].strip()
    
    f.readline()
    my_t    = f.readline().split(';')[1][0:6]
            
    timestamp = datetime.strptime(my_date + '-' + my_t, "%Y%m%d-%H%M%S")

    f.close()

    wavelengths = hlp[:, 0]
    spectrum = hlp[:, 1]

    return (timestamp, wavelengths, spectrum)



def get_ccd_data(main_path, reload = False):

    my_times = []
    d = []

    #y = range(395, 500)
    #y = range(395, 1924)
    #y = range(3, 751)
    y = range(10, 584)


    if reload:
    
        for k in y:

            filename = 'test00000{0:04d}.csv'.format(k)

            (timestamp, wavelengths, spectrum) = get_single_file(main_path + filename)

            # get spectrum
            d.append(spectrum)

            my_times.append(timestamp)

        x = wavelengths


        output_arr = (x, np.array(y), np.array(my_times, dtype = np.datetime64), np.array(d))


        with open('spectrum_data.pickle', 'wb') as f:
            pickle.dump(output_arr, f)

    else:

        with open('spectrum_data.pickle', 'rb') as f:

            data_raw = pickle.load(f)

        output_arr = data_raw

    return output_arr


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
        try:
            
            ind = np.where( np.abs(t0 - d_f['times']) < timedelta(seconds = 20) )

            temp_arr.append(d_f['data'][ind[0][0], 1])

        except:

            print("Couldn't find time {0} in interval {1} - {2} ".format(t0, d_f['times'][0], d_f['times'][-1]))

    return np.array(temp_arr)



############################################################

# Potassium 769.9 nm, 766.5 nm (air)
# Potassium 770.1 nm, 766.7 nm (vac)

main_path = '/Users/boerge/Software/offline_furnace/'

reload = True #False

d_f = get_furnace_data(main_path)

(freq, y, ccd_times, d) = get_ccd_data(main_path, reload = reload)

temp_arr = find_temp_at_time(d_f, ccd_times)


#d2 = np.mean(d[0:200, :], axis = 0) - d[0, :]

d2 = np.mean(d[:, :], axis = 0) - 0*d[0, :]

#d3 = np.mean(d[200:400, :], axis = 0) - d[300, :]
#
#d4 = np.mean(d[500:700, :], axis = 0) - d[600, :]

plt.plot(freq, d2)

plt.figure()

plt.plot(freq, np.mean(d, axis = 0))

#plt.xlim(760, 780)

#plt.show()

#asd


(fig, ax) = plt.subplots(2, 1, figsize = (14,6))

ax[0].plot_date(ccd_times, temp_arr, '-')

ax[0].xaxis.set_major_formatter( DateFormatter('%H:%M') )

ax[0].set_xlim(min(ccd_times), max(ccd_times))


ind = np.where( np.abs(63.5 - temp_arr) < 0.25 )[0][0]

ax[0].axhline(temp_arr[ind], ls = '-', color = 'k')
ax[0].axvline(ccd_times[ind], ls = '-', color = 'k')

ax[1].pcolor(y - y[0], freq, np.transpose(d))


ax[1].set_xlabel('Spectrum Index')
ax[1].set_ylabel('Wavelength (nm)')



#plt.figure()
#
#for k in [3, 10, 20, 500]:
#
#    plt.plot(x, d[k], label = 'Temp {0} C'.format(temp_arr[k]))


plt.figure()

plt.plot(freq, np.mean(d[:, :], axis = 0))






(ts, wl, spec) = get_single_file(main_path + 'test00000{0:04d}.csv'.format(3108))

plt.figure()

plt.plot(wl, spec)



(ts, wl, spec) = get_single_file(main_path + 'icl.csv'.format())


plt.figure()

plt.plot(wl, spec)

(ts, wl, spec) = get_single_file(main_path + 'potassium.csv'.format())


plt.figure()

plt.plot(wl, spec)




plt.show()






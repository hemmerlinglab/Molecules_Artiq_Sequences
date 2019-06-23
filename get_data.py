import numpy as np
import datetime
import matplotlib.pyplot as plt
import os
import glob
import sys
from fit_yb import *

kB = 1.38e-23
c = 299792458
amu = 1.6605e-27
hbar = 1.05457e-34

def doppler2temp(sigma, f0 = 0.0, mass = 0.0):

    # sigma is the standard deviation of the Gaussian distribution exp(-x^2/2 sigma^2)
    return (sigma**2 * mass * c**2)/(kB * f0**2)

def av(arr, no_of_avg):
    # for 1D array
    if len(arr.shape)==1:
        hlp = np.zeros([int(arr.shape[0]/no_of_avg)])

        for k in range(len(hlp)):
            for m in range(no_of_avg):
                hlp[k] += arr[no_of_avg*k + m]

        return hlp/no_of_avg

    if len(arr.shape)==2:     

        # for 2D array
        hlp = np.zeros([int(arr.shape[0]/no_of_avg), arr.shape[1]])

        for k in range(len(hlp)):
            for m in range(no_of_avg):
                hlp[k] += arr[no_of_avg*k + m, :]

        return hlp/no_of_avg


def get_data(time_stamp = None, options = {}, basefilename =  '/home/molecules/github/data/' + str(datetime.datetime.today().strftime('%Y%m%d')) + '/' + str(datetime.datetime.today().strftime('%Y%m%d'))):        

    
    if time_stamp == None:
        # get latest time stamp
        all_files = np.sort(glob.glob(basefilename + "*"))
        time_stamp = all_files[-1].split('_')[1]
    
    print('Analysing ... ' + basefilename + time_stamp)
    
    f_freqs = basefilename + time_stamp + '_freqs'
    f_ch1 = basefilename + time_stamp + '_ch1'
    f_ch2 = basefilename + time_stamp + '_ch2'
    
    
    cut_time1 = options['t1'] # ms
    cut_time2 = options['t2'] # ms
    freq1_cut = options['nu1'] # MHz
    freq2_cut = options['nu2'] # MHz
    
    freqs = np.genfromtxt(f_freqs, delimiter=",")
    ch1 = np.genfromtxt(f_ch1, delimiter=",")
    ch2 = np.genfromtxt(f_ch2, delimiter=",")
    
    # get number of averages
    no_of_avg = int(len(freqs)/len(np.unique(freqs)))
    
    print('Found ' + str(no_of_avg) + ' averages.')
    
    freqs = av(freqs, no_of_avg)
    ch1 = av(ch1, no_of_avg)
    ch2 = av(ch2, no_of_avg)
    
    avg_freq = np.mean(freqs)
    
    nus = (freqs - avg_freq)*1e12/1e6
    
    delay_in_for_loop = 50e-6
    no_of_time_points = ch1.shape[1]
    times = np.arange(0, no_of_time_points) * (8.97e-6 + delay_in_for_loop) / 1e-3
    
    dt = times[1] - times[0]
    dnu = nus[1] - nus[0]
    
    ch1_start = np.where( np.abs(times - cut_time1) < dt )[0][0]
    ch1_end = np.where( np.abs(times - cut_time2) < dt )[0][0]
    freq1_ind = np.where( np.abs(nus - freq1_cut) < dnu )[0][0]
    freq2_ind = np.where( np.abs(nus - freq2_cut) < dnu )[0][0]
    
    
    # subtracting the DC offset
    offset_avg_points = 5
    for k in range(ch1.shape[0]):
        ch1[k, :] = ch1[k, :] - np.mean(ch1[k, -offset_avg_points:-1])
        ch2[k, :] = ch2[k, :] - np.mean(ch2[k, -offset_avg_points:-1])
    
    # scaling the frequency axis to the blue
    nus = 2*nus
    avg_freq = 2*avg_freq
    
    
    spectrum = np.mean(ch1[:, ch1_start:ch1_end], axis = 1)
    
    (x_fit, y_fit, fit_result) = fit_yb(nus, spectrum)
    
    
    timetrace = np.mean(ch1[freq1_ind:freq2_ind, :], axis = 0)
    
    
    result = {'nus' : nus, 'spectrum' : spectrum, 'times' : times, 'timetrace' : timetrace, 'x_fit' : x_fit, 'y_fit' : y_fit, 'fit_result' : fit_result}
    return result
    
    
    
    

import numpy as np
import matplotlib.pyplot as plt

datafolder = '/home/molecules/software/data/'
basefolder = '20190806'
ch1_file = open(datafolder+basefolder+'/'+basefolder+'_155848_ch1','r')
data = np.genfromtxt(ch1_file,delimiter=',')
plt.figure()
plt.pcolor(np.transpose(data))
plt.show()

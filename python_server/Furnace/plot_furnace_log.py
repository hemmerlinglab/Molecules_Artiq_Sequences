import numpy as np
import matplotlib.pyplot as plt

import os


f = open('furnace_log.csv')

lines = f.readlines()

lines = lines[0].split(',')

print(lines[0:10])
T_set = np.array(lines[2::6], dtype = float)
T_act = np.array(lines[4::6], dtype = float)
out = lines[6::6]

plt.figure()

plt.plot(T_set)
plt.plot(T_act)

plt.show()

f.close()



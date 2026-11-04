import numpy as np
import scipy
from scipy.special import jv
import matplotlib.pyplot as plt


x = np.linspace(0, 4, 1000)

power = 38.5 # dBm
Z = 50 # Ohm

Vp = np.sqrt(2) * np.sqrt(Z * 10**(power/10)/1e3)

# modulation efficiency
kappa = 58 # mrad/Vp

beta = kappa * Vp * 1e-3 # rad

plt.figure()
plt.subplot(1,2,1)

n = 0
plt.plot(x, jv(n, x)**2)
n = 1
plt.plot(x, jv(n, x)**2)
n = 2
plt.plot(x, jv(n, x)**2)
n = 3
plt.plot(x, jv(n, x)**2)

plt.axvline(beta, ls = '--', color = 'k')

plt.xlabel('Modulation index (rad)')
plt.ylabel('Intensity')

plt.grid()

plt.subplot(1,2,2)

narr = np.arange(0, 4)

plt.plot(narr, jv(narr, beta)**2, 'o')

plt.xlabel('Sideband order')
plt.ylabel('Intensity')
plt.grid()

plt.tight_layout()

plt.show()



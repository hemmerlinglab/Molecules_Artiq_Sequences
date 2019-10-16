import numpy as np
import matplotlib
import matplotlib.pyplot as plt

'''
	The purpose of this script is to quantitatively compare the effects of doppler and pressure
broadaening on the in-cell spectral lines of an ablated ytterbium gas mixed with a Helium buffer
gas.  This combination is known as the voigt profile, a convolution of the gaussian doppler
broadening with the lorentzian pressure broadening.

Doppler broadening:

I(f) = Io*sqrt(4*ln(2)/pi)*(1/dfd)*exp(-4*ln(2)*(f-f0)^2/dfd^2)
dfd = 2*f0/c*sqrt(2*ln(2)*kb*T/M)



'''

amu = 1.6605390666050e-27 # kg
kb = 1.380649e-23 # J/K
c = 299792458 # m/s
M = np.array([170,171,172,173,174,176]) # ytterbium isotopes
iso_a = np.array([12.887, 31.896, 16.098, 16.098, 21.754, 14.216, 14.216, 3.023, 0.126]) # isotope abundances
iso_f = np.array([-508.89, 0, -250.78, 589.75, 531.11, 835.19, 1153.68, 1190.36, 1888.80])*10^6 # Hz isotope frequency shift

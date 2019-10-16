import matplotlib
import matplotlib.pyplot as plt
from fit_sin import *

fi = open('data_volt.txt')


volts = []
while True:
	try:
		volts.append(float(fi.readline()))
	except:
		break


fi.close()

fit_x = np.arange(599)
fit_y = volts

result = my_fit(fit_x, fit_y)

(mod_x, mod_y) = fcn2min(result.params, fit_x, [], return_plot = True)

print('Frequency:',result.params['freq'].value)
print('Amplitude:',result.params['amp'].value)
print('Delta:',result.params['dlt'].value)


plt.figure()
plt.plot(volts,'ro')
plt.plot(mod_y)
plt.show()

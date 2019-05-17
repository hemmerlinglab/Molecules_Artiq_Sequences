import matplotlib
import matplotlib.pyplot as plt
import numpy as np

v_name = 'signal_1.txt'
v_in = open(v_name,'r')
raw_vdata = v_in.read().split(' ')
v_in.close()


f_name = "fire_check_1.txt"
f_in = open(f_name,'r')
raw_fdata = f_in.read().split(' ')
f_in.close()

frchks = []
signal = []

for f in raw_fdata:
	try:
		frchks.append(float(f))
	except:
		pass

for v in raw_vdata:
	try:
		signal.append(float(v))
	except:
		pass

dt = np.arange(len(signal))*13.97e-3 # ms

plt.figure()
plt.plot(dt,signal,'b-')
plt.title('Absorption Signal')
plt.xlabel('Time (ms)')
plt.ylabel('Diode Voltage (V)')

plt.figure()
plt.plot(dt,frchks,'g-')
plt.title('YAG Fire Check')
plt.xlabel('Time (ms)')
plt.ylabel('Diode Voltage (V)')

plt.show()
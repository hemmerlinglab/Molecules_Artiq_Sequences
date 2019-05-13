import matplotlib
import matplotlib.pyplot as plt
import numpy as np

data = []
f_name = 'test2.txt'
f_in = open(f_name,'r')
string_data = f_in.read().split(' ')
#print(string_data)
for dat_pt in string_data:
	try:
		data.append(float(dat_pt))
	except:
		pass

in_peak = False
peak_start = []
for i in range(len(data)):
	if data[i] > 0:
		if not in_peak:
			in_peak = True
			peak_start.append(i)
		else:
			pass

	else:
		if in_peak:
			in_peak = False
		else:
			pass

dts = []
for idx in range(1,len(peak_start)):
	dts.append(1000/(peak_start[idx]-peak_start[idx-1]))



print('Peaks:',peak_start)
print('dt (us):',np.mean(dts))



plt.figure()
plt.plot(data)
plt.xlabel('Sample Number')
plt.ylabel('Voltage (V)')
plt.show()


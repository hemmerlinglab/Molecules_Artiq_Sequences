from artiq.experiment import *
import artiq.coredevice.sampler as spr


data_string = ''
f = open('data.txt')
reading = True
while reading:
	newdata = f.readline()
	if newdata != '':
		data_string += newdata
	else:
		reading = False

data_split = data_string.split('.')
data_strip = []
data = []
for d in data_split:
	try:
		data.append(int(d))

	except:
		data_strip.append(d)

volts = []
for da in data:
	volts.append(spr.adc_mu_to_volt(da))

fo = open('data_volt.txt','w')
for v in volts:
	fo.write(str(v)+'\n')



f.close()
fo.close()

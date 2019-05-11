import matplotlib
import matplotlib.pyplot as plt

fi = open('data_volt.txt')


volts = []
while True:
	try:
		volts.append(float(fi.readline()))
	except:
		break


fi.close()

plt.figure()
plt.plot(volts)
plt.show()

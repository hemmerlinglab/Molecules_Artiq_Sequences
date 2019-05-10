import matplotlib
import matplotlib.pyplot as plt

data_string = ''
f = open('data.txt')
reading = True
while reading:
	newdata = f.readline()
	if newdata != '':
		data_string += newdata
	else:
		reading = False

data = data_string.split('.')


print(data)
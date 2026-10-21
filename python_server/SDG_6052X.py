import socket #for socket
import sys #for exit
import numpy as np
import time #for sleep

class SDG_6052X:

	def __init__(self):
		IP = '192.168.42.87'
		PORT = 5025

		s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((IP, PORT))

		self.command_delay = 0.1

		self.socket = s

		return

	def close(Self):
		Self.socket.close()
		time.sleep(.500)

	def recv(self):
		self.msg = self.socket.recv(1024)
		return self.msg

	def send(self,msg):
		send_msg = msg + '\n'
		self.socket.send(send_msg.encode())
		time.sleep(self.command_delay)

	def query(self, msg, decode = True):
		self.send(msg)
		if decode:
			return self.recv().decode('utf-8').strip()
		else:
			return self.recv()


	def on(self, channel = 1):
		self.send("C{0}:{1}".format(channel, "OUTP ON")) 

	def off(self, channel = 1):
		self.send("C{0}:{1}".format(channel, "OUTP OFF"))

	def set_load(self, channel = 1, load = '50'):
		self.send('C{0}:{1} {2},{3}'.format(channel,"OUTP","LOAD", load))

	def set_BSWV(self, channel = 1, wavetype = "SINE",frequency = 200000, period = "PERI", amplitude = 500e-3):
		self.send('C{0}:BSWV WVTP,{1},FRQ,{2},AMP,{4}'.format(channel,wavetype, frequency, period, amplitude))

	def set_sine_wave(self, channel = 1, frequency = 200e3, amplitude  = 500e-3):
		self.send("C{0}:BSWV WVTP,SINE,FRQ,{1},AMP,{2}".format(channel, frequency, amplitude))

	def set_Burst(self, channel = 1, period = 1e-3):
		self.send("C{0}:BTWV STATE,ON,PERI,{1}".format(channel,period))

	def set_sweep(self, channel = 1, start = 250e3, duration = 3e-3, stop = 0, sweepmode = 'LINE',trigger = 'INT', direction = 'DOWN'):

		# amplitude needs to be constants at 640 mV

		amplitude = 640e-3

		self.send("C{0}:SWWV STATE,ON,CARR,WVTP,SINE,CARR,AMP,{4},TIME,{6},START,{1},STOP,{2},DIR,{7},SWMD,{3},TRSR,{5}".format(
			channel, 
			start, 
			stop, 
			sweepmode,
			amplitude, 
			trigger,
			duration,
			direction))

	def set_burst(self, channel = 1):
		self.send('C{}'.format(channel))




####Main#######
#Queries require question marks
if __name__ == '__main__':
	SDG = SDG_6052X()	
	SDG.on(channel =1)
	SDG.set_load(channel=1, load = '50')
	# SDG.set_sine_wave(channel = 1, frequency = 100e3, amplitude = 100e-3)
	SDG.set_sweep(channel = 1, start = 5e3, stop = 30e6)
	time.sleep(10e-3)
	print(SDG.query('*IDN?'))
	SDG.off(channel = 1)









	SDG.close()



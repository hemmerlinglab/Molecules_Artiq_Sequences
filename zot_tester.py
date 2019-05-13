import sys
import os
import select
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import time

class ZOT(EnvExperiment):
	def build(self):
		self.setattr_device('core')
		self.setattr_device('sampler0')
		self.setattr_device('zotino0')

	@kernel
	def zot_test(self,vlt):
		self.core.break_realtime()
		self.zotino0.init()
		delay(200*us)
		self.zotino0.write_dac(0,vlt) # args are channel,voltage
		delay(1*ms)
		self.zotino0.load()

	@kernel
	def get_sampler_voltages(self, sampler, cb):
		self.core.break_realtime()
		sampler.init()
		delay(50*ms)
		for i in range(8):
			sampler.set_gain_mu(i, 0)
			delay(100*us)
		smp = [0.0]*8
		sampler.sample(smp)
		cb(smp)


	def run(self):
		self.core.reset()
		print('Press ENTER to begin zotino test')
		input()
		set_max = 10
		set_min = -10
		set_pts = np.linspace(-10,10,201)
		data = []
		voltages = []
		def setv(x):
			nonlocal voltages
			voltages = x
		for j in range(len(set_pts)):
			self.zot_test(set_pts[j])
			self.get_sampler_voltages(self.sampler0, setv)
			data.append(voltages[0])
			print('Completed {}/{}'.format(j+1,len(set_pts)),end='\r')

		f_name = "zots.txt"
		f_out = open(f_name,'w')
		for k in range(len(data)):
			f_out.write(str(set_pts[k])+','+str(data[k])+' ')
		f_out.close()
		print('Data written to {}'.format(f_name))
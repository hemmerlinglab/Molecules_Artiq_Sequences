import sys
import os
import select
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import time
from simple_pid import PID
from wlm import *

class ZOT_LOCK(EnvExperiment):
	def build(self):
		self.setattr_device('core')
		self.setattr_device('zotino0')
		self.zotino0.init()
		self.set_zot(0.0)
		self.wlm = WavelengthMeter()
		self.setattr_argument('setpoint',NumberValue(default=382.110350,unit='THz',scale=1,ndecimals=6,step=.000001))
        self.setattr_argument('actual',NumberValue(default=))
        self.pid = PID(100,1000,0,self.setpoint)

	@kernel
	def set_zot(self,vlt):
		delay(200*us)
		self.zotino0.write_dac(0,vlt) # args are channel,voltage
		delay(1*ms)
		self.zotino0.load()

	def run(self):
		self.core.reset()
		while True:

			self.set_zot()

		f_name = "zots.txt"
		f_out = open(f_name,'w')
		for k in range(len(data)):
			f_out.write(str(set_pts[k])+','+str(data[k])+' ')
		f_out.close()
		print('Data written to {}'.format(f_name))
from artiq.experiment import *
import numpy as np
import time

class KILL(EnvExperiment):
	def build(self):
		self.setattr_device('core')
		self.setattr_device('scheduler')

	def run(self):
		self.set_dataset('parabola',np.full(10,np.nan),broadcast=True)
		j = 0
		while True:
			self.scheduler.pause()
			for i in range(10):
				self.mutate_dataset('parabola',i,i*i+j)
				time.sleep(0.5)

			j = j + 1



from artiq.experiment import *
import numpy as np
import time
from artiq.applets import *



class MgmtTutorial(EnvExperiment):
	def build(self):
		self.setattr_argument("count",NumberValue(default=10,ndecimals=0,step=1))

	def run(self):
		self.set_dataset("parabola",np.full(self.count,np.nan),broadcast=True)
		for i in range(self.count):
			self.mutate_dataset("parabola",i,i*i)
			print('Iteration: {}/{}'.format(i+1,self.count))
			time.sleep(0.5)

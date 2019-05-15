from artiq.experiment import *

class DAQ(EnvExperiment):
	def build(self):
		self.setattr_device('core')
		self.setattr_device('ttl4') # flash-lamp
		self.setattr_device('ttl6') # q-switch

	@kernel
	def ttl_test(self):
		self.core.break_realtime()
		for i in range(100):
			delay(999835*us)
			self.ttl4.pulse(15*us)
			delay(135*us)
			self.ttl6.pulse(15*us)


	def run(self):
		self.core.reset()
		j = 0
		while True:
			print('Press ENTER for trial {}'.format(j+1),end='')
			input()
			self.ttl_test()
			j+=1
			print('\r')
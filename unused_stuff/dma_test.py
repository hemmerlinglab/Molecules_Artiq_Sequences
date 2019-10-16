from artiq.experiment import *

class DMAPulses(EnvExperiment):
	def build(self):
		self.setattr_device('core')
		self.setattr_device('core_dma')
		self.setattr_device('ttl4')

	@kernel
	def record(self):
		with self.core_dma.record('pulses'):
			for i in range(50):
				self.ttl4.pulse(100*ns)
				delay(100*ns)

	@kernel
	def run(self):
		self.core.reset()
		self.record()
		pulses_handle = self.core_dma.get_handle('pulses')
		delay(5*ms)
		self.core.break_realtime()
		while True:
			self.core_dma.playback_handle(pulses_handle)
			delay(20*us)
from artiq.coredevice.ad9910 import * 
from artiq.experiment import *

class Zijue(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.cpld = self.get_device("urukul0_cpld")
		self.dds = self.get_device("urukul0_ch1")
		self.amp = [0.0, 0.1,0.2,0.3,0.4, 0.5, 0.6, 0.7,0.8, 0.9,1.0]

	@kernel	
	def run(self):
		self.core.reset()
		self.core.break_realtime()
		self.dds.init()
		self.dds.cpld.init()
		delay(5*us)
		self.dds.set(frequency = 1*MHz, amplitude = 1.0)
		self.dds.cfg_sw(False)
		
		
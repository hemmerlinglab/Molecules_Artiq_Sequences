from artiq.experiment import *
from artiq.coredevice.ad9910 import *
import numpy as np
import sys 


class practice(EnvExperiment):

	def build(self):
		self.setattr_device("core")
		self.setattr_device("ttl16") 
		#urukul ineherit or has the cpld so no need to define it again when geeting urukul0_ch1
		self.dds = self.get_device("urukul0_ch1")
		self.cpld = self.get_device("urukul0_cpld")
		# self.amp = np.linspace(1, 0, 100) 
		self.amp = [1.0, 0.9,0.8, 0.7,0.6, 0.5,0.4, 0.3 ,0.2,0.1, 0.0]
		# self.amp = [0.0, 0.0, 0.0, 0.7, 0.0, 0.7, 0.7] 
		self.asf_ram = [0]*len(self.amp) 

	# def prepare(self):
	# 	#prepare my parameters
	# 	#apparently asf_ram will read in reverse order
	# 	self.amp = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0] 
	# 	self.asf_ram = [0]*len(self.amp) 

	@kernel
	def init_dds(self):
		self.core.break_realtime()
		self.dds.init()
		self.cpld.init()
		# self.dds.cfg_sw(True)

	@kernel	
	def RAM_configure(self):
		self.core.break_realtime()
		#disable RAM mode before writing to the RAM
		self.dds.set_cfr1(ram_enable = 0)
		#Update the register profile after any RAM modification
		self.dds.cpld.io_update.pulse_mu(8)
		#set profile to default 
		self.dds.cpld.set_profile(0)
		#set the RAM profile settings
		self.dds.set_profile_ram(start = 0, end = len(self.asf_ram)-1, step = 250, profile = 0, mode=RAM_MODE_CONT_RAMPUP)
		# self.dds.set_profile_ram(start = 0, end = 30, step = 150, profile = 0, mode=RAM_MODE_CONT_RAMPUP)

		self.dds.cpld.io_update.pulse_mu(8)

		#converts amplitude values to RAM profile data 
		self.dds.amplitude_to_ram(self.amp, self.asf_ram)
		#write to the RAM
		self.dds.write_ram(self.asf_ram)
		self.core.break_realtime()
		self.dds.set(frequency = 2*MHz, amplitude = 1.0, profile = 0)
		# self.dds.set(frequency = 5*MHz, profile = 0)
	
		self.dds.cpld.io_update.pulse_mu(8)
		self.dds.set_cfr1(ram_enable = 1, ram_destination = RAM_DEST_ASF)
		self.dds.cpld.io_update.pulse_mu(8)



	@kernel
	def run(self):
		self.core.reset()
		self.core.break_realtime()
		self.ttl16.output()
		# self.cpld.init()
		self.init_dds()
		# self.dds.cfg_sw(True)


		delay(2*us)
		self.ttl16.pulse(1*us)
		self.dds.cfg_sw(True)

		delay(2*us)
		self.RAM_configure()

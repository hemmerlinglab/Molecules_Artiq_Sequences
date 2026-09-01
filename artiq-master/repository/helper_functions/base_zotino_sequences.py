from artiq.experiment import *

##########################################################################
# Zotino sampler functions
##########################################################################

@kernel
def set_zotino_voltage(self, channel, voltage):

    zotino_voltage = 5.0/30.0e3 * float(voltage)

    # software limit to 0V - +5V
    if zotino_voltage < 0:
        zotino_voltage = 0.0
    if zotino_voltage > 5.0:
        zotino_voltage = 5.0

    self.core.break_realtime()

    self.zotino0.init()
    delay(200*us)

    self.zotino0.write_gain_mu(channel, 65000)
    self.zotino0.load()
    delay(200*us)
    self.zotino0.write_dac(channel, zotino_voltage)
    self.zotino0.load()
    delay(200*us)

    return



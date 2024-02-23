from synth_hd import SynthHD


class Microwave():

    def __init__(self):

        self.device = SynthHD('/dev/Windfreak')

        self.device.init()

        # set device to external frequency reference
        self.device.reference_mode      = 'external'
        self.device.reference_frequency = 10.0e6

        self.off()

        return

    def freq(self, frequency, channel = 0):

        self.device[channel].frequency = frequency

        return

    def power(self, power, channel = 0):

        self.device[channel].power = power

        return

    def on(self, channel = 0):

        self.device[channel].enable = True

        return

    def off(self, channel = 0):

        self.device[channel].enable = False

        return

    def close(self):

        return






from synth_hd import SynthHD


class Microwave():

    def __init__(self):

        self.device = SynthHD('/dev/Windfreak')

        self.device.init()

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






#import pyvisa as visa
import visa

class BK9202():

    def __init__(self):        
        self.rm = visa.ResourceManager("@py")
        self.instr = self.rm.open_resource('USB0::65535::37376::802204020747010080::0::INSTR')

        self.instr.write("SYST:REM") # switch to remote mode

    def switch_on(self):
        self.instr.write("SOURCE:OUTPUT:STATE 1")

    def switch_off(self):
        self.instr.write("SOURCE:OUTPUT:STATE 0")

    def set_current(self, curr):
        self.instr.write("CURR:AMPL " + str(curr))

    def set_voltage(self, volt):
        self.instr.write("VOLT:AMPL " + str(volt))

    def close(self):

        self.instr.write("SYST:LOCAL") # switch to local mode
        self.instr.close()

if __name__ == '__main__':

    bk = BK9202()

    bk.set_current(2.3823)
    bk.set_voltage(1.534)

    #bk.switch_on()

    bk.close()


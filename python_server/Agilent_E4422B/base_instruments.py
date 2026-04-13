import os
import pyvisa as visa

os.add_dll_directory(r"C:\Program Files\Keysight\IO Libraries Suite\bin")

class base_gpib_instrument:

    def __init__(self, IP):

        self.rm = visa.ResourceManager('ktvisa32')
        #self.rm = visa.ResourceManager("@py")

        self.device = self.rm.open_resource('GPIB0::' + str(IP) + '::INSTR')

        return

    def id(self):

        print(self.query('*IDN?'))

        return

    def write(self, msg):

        self.device.write(msg)

        return

    def query(self, msg):

        return self.device.query(msg)

    def wait_finished(self):

        while not self.query('*OPC?') == '1':
            pass

        return

    def close(self):

        self.device.close()

        return






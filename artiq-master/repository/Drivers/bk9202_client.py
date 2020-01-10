import socket
import sys

class BK9202():

    def __init__(self):

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        #server_address = ('localhost', 10000)
        server_address = ('localhost', 65000)
        print('connecting to %s port %s' % server_address)
        self.sock.connect(server_address)

    def send(self, msg):
        self.sock.sendall(msg.encode())
        
    def switch_on(self):
        self.send("SOUR:OUTP:STAT 1 ")

    def switch_off(self):
        self.send("SOUR:OUTP:STAT 0 ")

    def set_current(self, curr):
        self.send("CURR:AMPL " + "{0:7.4f}".format(curr)) # need to send 17 bytes

    def set_voltage(self, volt):
        self.send("VOLT:AMPL " + "{0:7.4f}".format(volt))
    
    def open(self):
        self.send("SYST:REM         ") # switch to local mode

    def close(self):
        self.send("SYST:LOCAL       ") # switch to local mode
        self.sock.close()


if __name__ == '__main__':

    bk = BK9202()

    bk.open()

    bk.set_current(2.3823)
    bk.set_voltage(11.534)

    #bk.switch_on()

    bk.close()





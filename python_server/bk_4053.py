import socket
import time
import numpy as np


class BK4053:
    
    def __init__(self):

        TCP_IP = '192.168.42.82'
        TCP_PORT = 5024
        TCP_PORT = 5025

        self.command_delay = 0.1

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        s.connect((TCP_IP,TCP_PORT))
   
        self.socket = s

        return
   
    def close(self):

        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

        return

 
    def send(self, msg):

        send_msg = msg + '\n'

        self.socket.send(send_msg.encode())

        time.sleep(self.command_delay)

    def recv(self):

        self.msg = self.socket.recv(1024)

        return self.msg

    def query(self, msg, decode = True):
        
        self.send(msg)

        if decode:
            return self.recv().decode('utf-8').strip()
        else:
            return self.recv()

    def on(self, ch):

        self.send("C{0}:{1}".format(ch, 'OUTP ON'))

    def off(self, ch):

        self.send("C{0}:{1}".format(ch, 'OUTP OFF'))

    def read_status(self, channel):
        
        return self.query('C{0}:{1}'.format(channel, 'BSWV?'))

    def read_arwv(self, channel):
        
        return self.query('C{0}:{1}'.format(channel, 'ARVW?'))

    def set_arwv(self, channel, index):
        
        self.send('C{0}:{1}{2}'.format(channel, 'ARWV INDEX,', index))

    def set_load(self, channel, load):
        
        # load = 50 or HZ
        self.send('C{0}:{1}{2}'.format(channel, 'OUTP LOAD,', load))

    def set_dc_output(self, channel, voltage, load = 'HZ'):
        
        self.set_load(channel, load)
        
        self.send('C{0}:BSWV WVTP,DC,OFST,{1}'.format(channel, voltage))

        return

    def set_sine_output(self, channel, freq = 1, amplitude = 10e-3, load = '50'):

        # freq in MHz
        # amplitude in V
        
        self.set_load(channel, load)
        
        self.send('C{0}:BSWV WVTP,SINE,FRQ,{1},AMP,{2}'.format(channel, freq*1e6, amplitude))

        return






if __name__ == '__main__':

    bk = BK4053()

    # Mixer test
    # Output DC voltage in channel 1
    bk.set_dc_output(1, 0.5)
    bk.on(1)

    #bk.set_load(1, 'HZ')
    #bk.send('C1:ARWV INDEX,12')
    #bk.send('C1:BSWV WVTP,ARB,AMP,0.5')
    #bk.on(1)


    #print(bk.read_status(1))
    #print(bk.read_status(2))
    #
    #print(bk.query('C1:OUTP?'))
    #print(bk.query('C2:OUTP?'))

    #bk.off(1)
    #bk.off(2)
    #bk.on(2)

    #print(bk.query('C1:OUTP?'))
    #print(bk.query('C2:OUTP?'))


    #print(bk.read_status(1))
    #print(bk.read_status(2))
    
    #bk.set_load(1, 'HZ')

    # bk.send('C2:BSWV FRQ,100,AMP,0')
    #
    ## bk.send('C2:ARWV INDEX,12')
    #
    ## bk.send('C2:BSWV WVTP,ARB')

    # bk.send('C2:BTWV STATE, OFF,PRD,.05,TRSR,INT,TRMD,OFF')
    # bk.send('C2:BTWV?')
    #
    # print(bk.read_status(2)
    
    #print(bk.query('Storelist?'))
    
    #print(bk.query('WVDT? M50', decode = False))


    #bk.set_arwv(2, 2)
    #print(bk.read_arwv(2))


    bk.close()



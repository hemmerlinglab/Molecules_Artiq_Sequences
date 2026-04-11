import serial
import time
import wlm

# Commands: (for query)
#   ID?     Gets the switch's ID string
#   CF?     Gets the input/output dimensions
#   EO      Sets the echo option
#   ER?     Gets the system's error state
#       +0      All is well
#       001
#       002
#       003
#   I1 (n)  Sets the output channel (n within range of dimensions)
#   I1?     Gets the current output channel
#   PK      Sets the switch to parking state

class Fiber():

    ################################
    
    def __init__(self,port):
    
        # Serial config
        
        self.bps = 115200 # bits per second (baud rate)
        self.dbs = 8 # data bits per baud
        self.sbs = 1 # stop bits
        self.term = b'\r' # terminator
        self.port = port # serial com port for motor
        self.ser = serial.Serial(self.port,baudrate=self.bps,timeout=1.0,parity=serial.PARITY_NONE,stopbits = serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
        
        self.cycling = False

  
    ################################
    
    def query(self, command):
    
        if type(command) != 'str':
            command = str(command)

        self.ser.write(command.encode('ascii')+self.term)
        
        time.sleep(0.005)

        if '?' in command:
            res = self.listen()
            return res


    ################################
    
    def listen(self):
        
        try:
            ret = self.ser.read(4).decode()
            listening = True
            while listening:
                if '\r\n>' in ret:
                    listening = False
                    return ret.split('\r\n>')[0][-1]
                else:
                    newret = self.ser.read(4).decode()
                    ret = ret + newret
        except:
            print('you need new ears')


    ################################

    def id(self):
        
        self.query('ID?')
        
        return
    

    ################################

    def get_output_channel(self):
        
        self.query('I1?')

        return
    

    ################################
    
    def setchan(self,channel):
        
        self.query('I1 '+str(channel))

        return

    
    ################################
    
    def getchan(self):
    
        res = self.query('I1?')
        
        return res

    
    ################################
    
    def cycle(self,channels):
    
        self.cycling = True
        
        print('Cycling {}'.format(channels))
        
        while self.cycling:
            for chan in channels:
                self.setchan(chan)
                time.sleep(.5)


    ################################
    
    def close(self):
    
        self.setchan(1)

        return





import socket
import sys
import pyvisa as visa

class BK9202():

    def __init__(self):        
        self.rm = visa.ResourceManager("@py")
        self.instr = self.rm.open_resource('USB0::65535::37376::802204020747010080::0::INSTR')

        #self.instr.write("SYST:REM") # switch to remote mode

    def send(self, msg):
        self.instr.write(msg)
        #print(msg)

class socket_server():

    def __init__(self, dev):

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', 65000)
        print('starting up on %s port %s' % server_address)
        self.sock.bind(server_address)

        # Listen for incoming connections
        self.sock.listen(1)

        self.device = dev

    def activate(self):

        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = self.sock.accept()
    
            try:
                print('connection from', client_address)
    
                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(17)
                    print('received "%s"' % data)
                    if data:
                        #print('Adjusting power supply.')
                        print('sending')
                        self.device.send(str(data.decode()))

                    else:
                        print('no more data from', client_address)
                        break
                
            finally:
                # Clean up the connection
                connection.close()




if __name__ == '__main__':

    bk = BK9202()

    server = socket_server(bk)

    server.activate()




import socket
import sys
import numpy as np
from wlm import *

# create conex objects
wlm = WavelengthMeter()


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.42.20', 62500)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
            print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        #while True:
            data = connection.recv(16)
            print('received request "%s"' % data)

            if data:
                data = a.GetFrequency()
                print('Sending frequencies')
                connection.sendall(data)
            else:
                print('no more data from', client_address)
                break
			
			
            
    finally:
        # Clean up the connection
        connection.close()


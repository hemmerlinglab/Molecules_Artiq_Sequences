import socket
import sys
import numpy as np
from ConexCC import *


# create conex objects
print('Initiating mirrors ....')
(cx, cy) = init_for_target_mapping()



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.42.20', 62000)
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
            print('received "%s"' % data)

            vals = data.decode().split('/')
            if len(vals)==2:
               x = np.float(vals[0])
               y = np.float(vals[1])
               print('Moving mirrors to ... ' + str(x) + '/' + str(y))
               # moving to absolute positions
               cx.query(1,'PA', str(x))
               cy.query(1,'PA', str(y))
			   
               print('x @ ' + str(cx.TP()))
               print('y @ ' + str(cy.TP()))


            #if data:
            #    print('sending data back to the client')
            #    connection.sendall(data)
            #else:
            #    print('no more data from', client_address)
            #    break
			
			
            
    finally:
        # Clean up the connection
        connection.close()


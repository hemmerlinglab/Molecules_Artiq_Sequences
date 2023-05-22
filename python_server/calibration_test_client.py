import socket
import sys
import numpy as np

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
#server_address = ('localhost', 10000)
server_address = ('192.168.42.20', 62500)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    
    # Send data
    message = 'henecal'
    print('sending "%s"' % message)
    sock.sendall(message.encode())
    
    # send hene frequency
    message = '473.612463'
    sock.sendall(message.encode())


finally:
    print('closing socket')
    sock.close()




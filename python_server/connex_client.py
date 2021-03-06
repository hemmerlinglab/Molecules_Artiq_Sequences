import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
#server_address = ('localhost', 10000)
server_address = ('192.168.42.20', 62000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    
    print(sys.argv[1])
    print(sys.argv[2])

    # Send data
    message = '4.7/5.7' # 3.5 - 4.5/4.25 and 4.0/3.0 - 5.0
    message = sys.argv[1] + '/' + sys.argv[2] # 3.5 - 4.5/4.25 and 4.0/3.0 - 5.0
    print('sending "%s"' % message)
    sock.sendall(message.encode())

    ## Look for the response
    #amount_received = 0
    #amount_expected = len(message)
    
    #while amount_received < amount_expected:
    #    data = sock.recv(16)
    #    amount_received += len(data)
    #    print('received "%s"' % data)

finally:
    print('closing socket')
    sock.close()




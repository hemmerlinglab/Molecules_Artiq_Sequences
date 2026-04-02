import socket


#############################################################
# Socket Helpers
#############################################################

def create_socket(ip, port, type = 'listen'):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (ip, port)
    print('starting up on %s port %s' % server_address)

    if type == 'listen':

        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)

    elif type == 'connect':
    
        sock.connect(server_address)

    else:

        pass

    return sock


def bind_socket(ip, port):

    # Creates and binds a socket and sets it to listen

    sock = create_socket(ip, port, type = 'listen')

    return sock


def connect_and_send_socket(ip, port, msg):

    # Connects to a socket and send a msg

    sock = create_socket(ipm, port, type = 'connect')

    sock.sendall(message.encode())
  
    return sock





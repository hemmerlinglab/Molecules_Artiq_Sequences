import numpy as np
import matplotlib.pyplot as plt
import socket

import time

from rigol import Rigol_RSA3030

from rigol_dho924 import Rigol_DHO924


def get_wavemeter_readings():

    # reads out laser frequencies from wavemeter

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.42.20', 62200)

    sock.connect(server_address)

    try:    
        # Request data
        message = 'request'
        #print('sending "%s"' % message)
        sock.sendall(message.encode())

        len_msg = int(sock.recv(2).decode())

        data = sock.recv(len_msg)

    finally:
        sock.close()

    # return a list of freqs
    # currently only one frequency is returned
    freqs = float(data.decode())

    #print('Getting laser frequencies ... {0:.6f} THz'.format(freqs))
    
    return freqs







if __name__ == "__main__":


    scope = Rigol_DHO924()
    spec  = Rigol_RSA3030()

    spec.set_freq([5e6, 120e6])

    fspec = open('freq_spec.dat', 'w')
    ferr = open('freq_err.dat', 'w')
    fwm = open('freq_wm.dat', 'w')
    ffast = open('freq_fast.dat', 'w')

    fspec.close()
    ferr.close()
    fwm.close()

    for n in range(25000):

        fspec = open('freq_spec.dat', 'a')
        ferr = open('freq_err.dat', 'a')
        fwm = open('freq_wm.dat', 'a')
        ffast = open('freq_fast.dat', 'a')

        wm = get_wavemeter_readings()

        s = spec.get_trace()
        x = s[:, 0]
        y = s[:, 1]

        err = scope.get_trace(4)
        fast = scope.get_trace(3)

        np.savetxt(fspec, [x], delimiter=',')
        np.savetxt(fspec, [y], delimiter=',')
        
        np.savetxt(fwm, [wm], delimiter=',')
        np.savetxt(ferr, [np.mean(err)], delimiter=',')
        
        np.savetxt(ffast, [np.mean(fast)], delimiter=',')

        time.sleep(5.0)

        print("{0} {1}".format(n, wm))
        
        fspec.close()
        ferr.close()
        fwm.close()
        ffast.close()

    scope.close()
    spec.close()


    plt.figure()

    plt.plot(x, y)

    plt.figure()
    plt.plot(err)

    plt.show()


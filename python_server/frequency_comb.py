from toptica.lasersdk.client import Client, NetworkConnection



# Toptica Frequency Comb'

class DFC():
    
    def __init__(self, IP = '192.168.42.42'):
    
        self.dev = Client(NetworkConnection(IP))
        
        self.open()

        return

    def open(self):

        self.dev.open()

        return

    def close(self):

        self.dev.close()

        return

    def id(self):

        print(self.dev.get('system-label', str))

        return

    def get_freq_diff(self):
        
        return self.dev.get('sys_def:RepRateLock:frequency_difference', float)

    def get_frep(self):
        
        return self.dev.get('sys_def:RepRateLock:internal_frep_counter', float)


##################################################################################################
# Main
##################################################################################################

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import numpy as np

    dfc = DFC()

    dfc.id()
    
    wr = []
    w_diff = []
    for k in range(1000):
        wr.append(dfc.get_frep())
        w_diff.append(dfc.get_freq_diff())
    
    wr = np.array(wr)
    w_diff = np.array(w_diff)

    dfc.close()

    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(wr - 200e6)
    plt.subplot(2,1,2)
    plt.plot(w_diff)

    plt.show()

    



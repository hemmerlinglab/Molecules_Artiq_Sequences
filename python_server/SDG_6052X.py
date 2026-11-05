import socket #for socket
import sys #for exit
import numpy as np
import time #for sleep
import binascii
import struct
import matplotlib.pyplot as plt
import pickle

class SDG_6052X:
    
    def __init__(self):
        IP = '192.168.42.87'
        PORT = 5025
        
        s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP, PORT))
        
        self.command_delay = 0.1
        
        self.socket = s
        
        # set max amplitude of both channels
        self.set_max_amplitude(amplitude = 2*640e-3) # note that there is a bug in the machine: it actually stores Vpp not Vp
        
        with open("/home/molecules/software/Molecules_Artiq_Sequences/python_server/amplifier_spline.pkl", "rb") as f:
            self.compensated_amp = pickle.load(f)
        
        return
    
    def close(Self):
        Self.socket.close()
        time.sleep(.500)
    
    def recv(self):
        self.msg = self.socket.recv(1024)
        return self.msg
    
    def send(self,msg):
        send_msg = msg + '\n'
        self.socket.send(send_msg.encode())
        time.sleep(self.command_delay)
    
    def query(self, msg, decode = True):
        self.send(msg)
        if decode:
            return self.recv().decode('utf-8').strip()
        else:
            return self.recv()

    ###########################################################
    # Device functions
    ###########################################################
    
    def on(self, channel = 1):
        self.send("C{0}:{1}".format(channel, "OUTP ON")) 

    def off(self, channel = 1):
        self.send("C{0}:{1}".format(channel, "OUTP OFF"))

    def set_load(self, channel = 1, load = '50'):
        self.send('C{0}:{1} {2},{3}'.format(channel,"OUTP","LOAD", load))

    def set_BSWV(self, channel = 1, wavetype = "SINE",frequency = 200000, period = "PERI", amplitude = 500e-3):
        self.send('C{0}:BSWV WVTP,{1},FRQ,{2},AMP,{4}'.format(channel,wavetype, frequency, period, amplitude))

    def set_sine_wave(self, channel = 1, frequency = 200e3, amplitude = 500e-3):
        self.send("C{0}:BSWV WVTP,SINE,FRQ,{1},AMP,{2}".format(channel, frequency, amplitude))

    def set_burst(self, channel = 1, period = 1e-3):
        self.send("C{0}:BTWV STATE,ON,PERI,{1}".format(channel,period))

    def set_arb(self, channel = 1):
        self.send("C{0}:BSWB WVTP,ARB")

    def set_sweep(self, channel = 1, start = 250e3, duration = 1000e-3, stop = 0, sweepmode = 'LINE',trigger = 'INT', direction = 'DOWN'):

        # amplitude needs to be constants at 640 mV
        
        amplitude = 640e-3
        
        self.send("C{0}:SWWV STATE,ON,CARR,WVTP,SINE,CARR,AMP,{4},TIME,{6},START,{1},STOP,{2},DIR,{7},SWMD,{3},TRSR,{5}".format(
            channel, 
            start, 
            stop, 
            sweepmode,
            amplitude, 
            trigger,
            duration,
            direction))

    def set_max_amplitude(self, amplitude = 1e-3):
        
        channel = 1
        self.send("C{0}:BSWV MAX_OUTPUT_AMP,{1}".format(channel, amplitude))
        channel = 2
        self.send("C{0}:BSWV MAX_OUTPUT_AMP,{1}".format(channel, amplitude))
        
        return


    ###########################
    # AWG    
    ###########################
  
    def send_binary_awg_data(self, data, channel, duration, wave_name):

        ###################################################
        # convert data to binary and send to AWG
        ###################################################

        # numpify and normalize data to 2**15

        data   = 32767 * data/np.max(np.abs(data))
        b_data = [self.int_to_two_byte_small_endian(int(num)) for num in data]

        final_byte_data = b''.join(b_data) + b'\n'

        freq = 1.0/duration

        cmd = 'C{0}:WVDT WVNM,{1},AMPL,0.64,OFST,0.0,FREQ,{2},WAVEDATA,'.format(
                channel,
                wave_name,
                freq
                )

        cmd = bytes(cmd, 'utf-8') + final_byte_data

        self.socket.send(cmd)
        time.sleep(self.command_delay)
        
        return

    ##########################################################

    def int_to_two_byte_small_endian(self, n):

        return struct.pack('<h', n)
   
    ##########################################################
    
    def linear_ramp(self, t, start, stop, duration):
    
        return np.array(start + (stop - start)/duration * t)
    
    ##########################################################
    
    def calculate_arb_wave(
            self,
            start_freq, 
            end_freq, 
            start_amp,
            stop_amp,
            duration
            ):
    
        num_points = 16384
        
        t = np.linspace(0, duration, num_points)
 
        # get linear A ramp - might need to change to other type of ramp    
        A_ramp = self.linear_ramp(t, start_amp, stop_amp, duration)
        
        # get linear frequency ramp
        f_ramp = self.linear_ramp(t, start_freq, stop_freq, 2.0 * duration)
    
        # define arb wave    
        y = A_ramp * np.sin( 2*np.pi * f_ramp * t )
   
        #import matplotlib.pyplot as plt
        #plt.plot(t, y)
        #plt.show()

        return np.array(y)


    def compensated_arb_wave(
            self,
            start_freq,
            stop_freq,
            max_amp,
            duration
            ):
 
        num_points = 16384
        
        t = np.linspace(0, duration, num_points)
    
        freq_ramp = self.linear_ramp(t, start_freq, stop_freq, duration)

        A_comp = max_amp * self.compensated_amp(freq_ramp / 1e6)
    
        y = A_comp * np.sin(np.pi * (freq_ramp + start_freq) * t)

        return np.array(y)


    def upload_comp_arb_wave(
            self,
            channel,
            start_freq, 
            stop_freq, 
            comp_amp,
            duration,
            wave_name = 'custom1'
            ):
        
        data = self.compensated_arb_wave(start_freq, stop_freq, comp_amp, duration)
        
        self.send_binary_awg_data(data, channel, duration, wave_name)
        
        return
   
    def upload_arb_wave(
            self,
            channel,
            start_freq, 
            stop_freq, 
            start_amp,
            stop_amp,
            duration,
            wave_name = 'custom1'
            ):
                
        data = self.calculate_arb_wave(start_freq, stop_freq, start_amp, stop_amp, duration)

        self.send_binary_awg_data(data, channel, duration, wave_name)

        return
   
    def start_awg(
            self, 
            channel, 
            wave_name = 'custom1',
            trigger   = 'MAN'
            ):
    
        #wave_name = 'Sine'
        #wave_name = 'StairDn'
        
        cmd = 'C{0}:ARWV NAME,{1}'.format(
            channel, 
            wave_name)
        
        #wave_number = 2
        #
        #cmd = 'C{0}:ARWV INDEX,{1}'.format(
        #    channel, 
        #    wave_number)

        self.send(cmd)
        
        self.send(f'C{channel}:BTWV STATE,ON')  # Turn burst mode ON
        self.send(f'C{channel}:BTWV GATE_NCYC,NCYC')  # N-Cycle mode (not Gated)
        self.send(f'C{channel}:BTWV TIME,1')  # Number of cycles = 1
        self.send(f'C{channel}:BTWV TRSR,{trigger}')  # Set trigger source to Manual/Software
        self.send(f'C{channel}:BTWV TRMD,RISE')  # Set trigger source to Manual/Software
        self.send(f'C{channel}:BTWV DLAY,0')  # Set trigger source to Manual/Software

        return

###########################
# Main
###########################

if __name__ == '__main__':

    channel = 2

    SDG = SDG_6052X()   

    start_freq = 10e6 #e3
    stop_freq = 500e6

    start_amp = 640e-3
    stop_amp = 640e-3

    duration = 25e-3 #500e-6


    SDG.set_arb(channel = channel)
    
    SDG.upload_comp_arb_wave(
            channel,
            start_freq, 
            stop_freq, 
            start_amp,
            duration
            )


    #SDG.upload_arb_wave(
    #        channel,
    #        start_freq, 
    #        stop_freq, 
    #        start_amp,
    #        stop_amp,
    #        duration
    #        )
    
    SDG.start_awg(channel, 
            trigger = 'MAN')
    

    SDG.on(channel = channel)
    
    #SDG.set_sine_wave(channel = channel, frequency = 200, amplitude = 500e-3)
    
    SDG.send(f'C{channel}:BTWV MTRIG')

    #time.sleep(1)

    #SDG.off(channel = channel)

    SDG.close()


    plt.show()



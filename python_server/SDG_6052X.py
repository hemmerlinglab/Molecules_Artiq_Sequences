import socket #for socket
import sys #for exit
import numpy as np
import time #for sleep
import binascii
import struct



class SDG_6052X:
    
    def __init__(self):
    	IP = '192.168.42.87'
    	PORT = 5025
    
    	s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	s.connect((IP, PORT))
    
    	self.command_delay = 0.1
    
    	self.socket = s
    
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
    
    
    def on(self, channel = 1):
        self.send("C{0}:{1}".format(channel, "OUTP ON")) 

    def off(self, channel = 1):
        self.send("C{0}:{1}".format(channel, "OUTP OFF"))

    def set_load(self, channel = 1, load = '50'):
        self.send('C{0}:{1} {2},{3}'.format(channel,"OUTP","LOAD", load))

    def set_BSWV(self, channel = 1, wavetype = "SINE",frequency = 200000, period = "PERI", amplitude = 500e-3):
        self.send('C{0}:BSWV WVTP,{1},FRQ,{2},AMP,{4}'.format(channel,wavetype, frequency, period, amplitude))

    def set_sine_wave(self, channel = 1, frequency = 200e3, amplitude  = 500e-3):
        self.send("C{0}:BSWV WVTP,SINE,FRQ,{1},AMP,{2}".format(channel, frequency, amplitude))

    def set_Burst(self, channel = 1, period = 1e-3):
	    self.send("C{0}:BTWV STATE,ON,PERI,{1}".format(channel,period))

    def set_sweep(self, channel = 1, start = 250e3, duration = 3e-3, stop = 0, sweepmode = 'LINE',trigger = 'INT', direction = 'DOWN'):

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

    ###########################
    # AWG    
    ###########################
    
    def linear_ramp(self, t, start, stop, duration):
    
        return np.array(start + (stop - start)/duration * t)
    
    def calculate_arb_wave(
            self,
            t, 
            start_freq, 
            end_freq, 
            start_amp,
            stop_amp,
            duration
            ):
    
        # get linear A ramp - might need to change to other type of ramp    
        A_ramp = self.linear_ramp(t, start_amp, stop_amp, duration)
        
        # get linear frequency ramp
        f_ramp = self.linear_ramp(t, start_freq, stop_freq, duration)
    
        # define arb wave	 
        y = A_ramp * np.sin( 2*np.pi * f_ramp * t )
    
        return y
 
    #def convert_awg(self, wave_points):

    #    ans = binascii.unhexlify('')
    #    for a in wave_points:
    #        if a < 0:
    #            b = hex(abs(a) + 2**15)
    #        else:
    #            b = hex(a)
    #        b = b[2:]
    #        len_b = len(b)
    #        if (0 == len_b):
    #        	b = '0000'
    #        elif (1 == len_b):
    #        	b = '000' + b
    #        elif (2 == len_b):
    #        	b = '00' + b
    #        elif (3 == len_b):
    #        	b = '0' + b
    #        
    #        b = b[2:4] + b[:2] #change big-endian to little-endian

    #        try:
    #        	c = binascii.unhexlify(b)    #Hexadecimal integer to ASCii encoded string
    #        	ans += c
    #        except:
    #        	print(a)
    #  
    #        	print(hex(a))
    #        	print(b)
    #        	xfgn	

    #    return ans
 
    def int_to_two_byte_small_endian(self, n):

        return struct.pack('<h', n)
   
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
        
        freq = 1.0/duration
        
        num_points = 16384
        
        t = np.linspace(0, duration, num_points)

        y = self.calculate_arb_wave(t, start_freq, stop_freq, start_amp, stop_amp, duration)

        data = y

        ###################################################
        # convert data to binary and send to AWG
        ###################################################

        # numpify and normalize data to 2**15
        data = 32767 * np.array(data)/np.max(data)

        b_data = [self.int_to_two_byte_small_endian(int(num)) for num in data]

        final_byte_data = b''.join(b_data) + b'\n'

        cmd = 'C{0}:WVDT WVNM,{1},AMPL,0.2,OFST,0.0,FREQ,{2},WAVEDATA,'.format(
                channel,
                wave_name,
                freq
                )

        cmd = bytes(cmd, 'utf-8') + final_byte_data

        self.socket.send(cmd)
        time.sleep(self.command_delay)
        
        return

    def start_awg(
            self, 
            channel, 
            wave_name = 'custom1'
            ):

        #wave_name = 'Sine'

        cmd = 'C{0}:ARWV NAME,{1}'.format(
            channel, 
            wave_name)
        
        self.send(cmd)
        
        self.send(f'C{channel}:BTWV STATE,ON')  # Turn burst mode ON
        self.send(f'C{channel}:BTWV GATE_NCYC,NCYC')  # N-Cycle mode (not Gated)
        self.send(f'C{channel}:BTWV TIME,1')  # Number of cycles = 1
        self.send(f'C{channel}:BTWV TRSR,MAN')  # Set trigger source to Manual/Software
        #self.send(f'C{channel}:BTWV STATE,OFF')  # Turn burst mode ON

        return


###########################
# Main
###########################

if __name__ == '__main__':

    channel = 2

    SDG = SDG_6052X()	

    start_freq = 10
    stop_freq = 10e3

    start_amp = 640e-3
    stop_amp = 240e-3

    duration = 10e-3


    SDG.upload_arb_wave(
            channel,
            start_freq, 
            stop_freq, 
            start_amp,
            stop_amp,
            duration
            )

    SDG.start_awg(channel)

    #print(SDG.query('C2:BTWV?'))
    

    SDG.on(channel = channel)
    
    #SDG.on(channel = channel)
	#
    #SDG.set_load(channel = channel, load = '50')
	#
    # SDG.set_sine_wave(channel = channel, frequency = 100e3, amplitude = 100e-3)
	#
    #SDG.set_sweep(channel = channel, start = 5e3, stop = 30e6)
	#
    #time.sleep(10e-3)
	#
    #print(SDG.query('*IDN?'))
    
    #print(SDG.query('STL? USER'))
	
    SDG.send('C2:BTWV MTRIG')

    SDG.off(channel = channel)

    SDG.close()



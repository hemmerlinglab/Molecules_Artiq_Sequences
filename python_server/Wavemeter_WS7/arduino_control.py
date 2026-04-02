import serial
import numpy as np


###################################################################
# Arduino Control Functions
###################################################################

def init_arduinos(com_ports, zero_init_output = False):

    ser_connections = {}
    for port in com_ports.keys():

        serial_port = com_ports[port] 

        baud_rate = 9600 

        try:
            ser = serial.Serial(serial_port, baud_rate, 
                                bytesize=serial.SEVENBITS, 
                                parity=serial.PARITY_ODD, 
                                stopbits=serial.STOPBITS_ONE, 
                                timeout=1)
        except:
            try:
                ser.close()
            except:
                print ("Serial port already closed" )
            ser = serial.Serial(serial_port, baud_rate, 
                                bytesize=serial.SEVENBITS, 
                                parity=serial.PARITY_ODD, 
                                stopbits=serial.STOPBITS_ONE, 
                                timeout=1)
    
        if zero_init_output:
            send_arduino_control(ser, 0.0, 1)
            send_arduino_control(ser, 0.0, 2)
    
        ser_connections[port] = ser

    return ser_connections


###############################################

def send_arduino_control(ser, control, channel, max_output = 4095.0):

    #print(control)
    # channel = which arduino DAC channel

    ard_mess =  int(max_output/20.0 * control + max_output/2.0)*10 + channel

    mystr = '{:05d}'.format(ard_mess).encode('utf-8')
    ser.write(mystr) # converts from unicode to bytes        

    return





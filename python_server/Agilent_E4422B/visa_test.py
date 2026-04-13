import pyvisa
import os

import os
#os.add_dll_directory(r"C:\Program Files (x86)\Keysight\IO Libraries Suite\bin")
os.add_dll_directory(r"C:\Program Files\Keysight\IO Libraries Suite\bin")

import pyvisa
rm = pyvisa.ResourceManager('ktvisa32')
print(rm.list_resources())





print('\n' * 3)
print('*' * 50)
print('\n' * 1)

try:
    rm_ni = pyvisa.ResourceManager("C:\\Windows\\System32\\visa32.dll")

    print(f"NI-VISA found: {rm_ni.list_resources()}")

except:

    print('didnt work')

print('*' * 50)
print('\n' * 3)

p = r'C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\ktvisa\\ktbin\\visa32.dll'
rm_ks = pyvisa.ResourceManager(p)



print(f"Keysight found: {rm_ks.list_resources()}")



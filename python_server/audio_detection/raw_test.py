import sounddevice as sd
from time import sleep
from gpiozero import LED

duration = 20.5  # seconds


def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    #print(max(indata[:, 1]))
    #print(len(indata[:, 1]))
    outdata[:] = indata

    if max(indata[:, 1])>0.025:
        print('hallo')
        led = LED(17)
        led.on()
        sleep(0.01)
        led.off()

with sd.Stream(channels=2, callback=callback):
    sd.sleep(int(duration * 1000))




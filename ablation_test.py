# use 'artiq-run' command
import sys
import os
import select
from artiq.experiment import *
from artiq.coredevice.ad9910 import AD9910
from artiq.coredevice.ad53xx import AD53xx

if os.name == 'nt':
    import msvcrt

def print_underflow():
    print('RTIO underflow occured')

def chunker(seq, size):
    res = []
    for el in seq:
        res.append(el)
        if len(res) == size:
            yield res
            res = []
    if res:
        yield res


def is_enter_pressed() -> TBool:
    if os.name == "nt":
        if msvcrt.kbhit() and msvcrt.getch() == b"\r":
            return True
        else:
            return False
    else:
        if select.select([sys.stdin, ], [], [], 0.0)[0]:
            sys.stdin.read(1)
            return True
        else:
            return False

class DAQ(EnvExperiment):
    def build(self):
        if self.get_device("scheduler").__class__.__name__ != "DummyScheduler":
            raise NotImplementedError(
                "must be run with artiq_run to support keyboard interaction")

        self.setattr_device('core')
        #self.setattr_device('ttl10') # experiment start
        #self.setattr_device('ttl4') # flash-lamp
        #self.setattr_device('ttl6') # q-switch
        self.setattr_device('sampler0')
        
        for k in range(4,24):
            self.setattr_device('ttl' + str(k)) # experiment start

    @kernel
    def get_sampler_voltages(self,sampler,cb):
        print('start sample')
        self.core.break_realtime()
        sampler.init()
        delay(5*ms)
        sampler.set_gain_mu(0,0)
        delay(100*us)
        # for i in range(8):
        #     sampler.set_gain_mu(i,0)
        #     delay(100*us)
        smp = [0.0]*8
        sampler.sample(smp)
        cb(smp)

    def test_sampler(self):
        voltages = []
        #print("asd")
        def setv(x):                        
            nonlocal voltages
            voltages = x                        
        #print("asd2")        
        self.get_sampler_voltages(self.sampler0,setv) # stuck here

        print("asd3")
        for voltage in voltages:
            print(voltage)
        #print("asd")

    #@kernel
    def run(self):
        self.core.reset()
        
        #self.ttl4.off()
        #self.ttl6.off()
        delay(35*us)
        self.test_sampler()

#        try:            
#            while True:
#    
#                with parallel:
#                    with sequential:
#                        #self.ttl11.pulse(5*us)
#                        self.ttl10.pulse(5*us)
#                        #for k in range(4, 64):
#                        #    eval('self.ttl' + str(k) + '.pulse(5*us)')
#                        #self.ttl12.pulse(5*us)
#                        delay(30*us)
#                        self.ttl4.pulse(5*us)
#                        delay(30*us)
#                        self.ttl4.pulse(5*us)
#                        delay(100*us)
#                    with sequential:
#                        delay(35*us)
#                        self.ttl6.pulse(5*us)
#                        delay(20*us)
#                        self.ttl6.pulse(5*us)
#
#                        self.test_sampler()
#
#                        #print("Start experiment")            
#                        delay(1000*ms)
#
#        except RTIOUnderflow:
#            print_underflow()

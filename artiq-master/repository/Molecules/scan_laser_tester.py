# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime
import os
import time
import csv

#### NO YAG!!!  no yag triggers, no check to see if yag fired


# every Experiment needs a build and a run function
class EXPERIMENT_1_TEST(EnvExperiment):
    def build(self):
        self.setattr_device('core') # Core Artiq Device (required)
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('ttl5') # uv ccd trigger
        self.setattr_device('sampler0') # adc voltage sampler
        self.setattr_device('scheduler') # scheduler used
        # EnvExperiment attribute: number of voltage samples per scan
        self.setattr_argument('scope_count',NumberValue(default=400,ndecimals=0,step=1))
        self.setattr_argument('scan_count',NumberValue(default=2,ndecimals=0,step=1))
        self.setattr_argument('setpoint_count',NumberValue(default=10,ndecimals=0,step=1))
        self.setattr_argument('setpoint_offset',NumberValue(default=375.76354,ndecimals=6,step=.000001))
        self.setattr_argument('setpoint_min',NumberValue(default=-500,ndecimals=0,step=1))
        self.setattr_argument('setpoint_max',NumberValue(default=500,ndecimals=0,step=1))
        self.setattr_argument('slowing_set',NumberValue(default = 375.76354,ndecimals=6,step=.000001))
        
    ### Script to run on Artiq
    # Basic Schedule:
    # 1) Trigger YAG Flashlamp
    # 2) Wait 150 us
    # 3) Trigger Q Switch
    # 4) In parallel, read off 2 diodes and PMT
    @kernel
    def fire_and_read(self):
        self.core.break_realtime() # sets "now" to be in the near future (see Artiq manual)
        self.sampler0.init() # initializes sampler device
        
        ### Set Channel Gain 
        for i in range(8):
            self.sampler0.set_gain_mu(i,0) # (channel,setting) gain is 10^setting
        
        delay(150*us)
        
        ### Data Variable Initialization
        data0 = [0]*self.scope_count # signal data
        data1 = [0]*self.scope_count # fire check data
        data2 = [0]*self.scope_count # uhv data
        data3 = [0]*self.scope_count # post select, checks blue
        #data4 = [0]*self.scope_count # unused for now
        #data5 = [0]*self.scope_count # unused for now
        #data6 = [0]*self.scope_count # unused for now
        #data7 = [0]*self.scope_count # unused for now
        smp = [0]*8 # individual sample

        ### Fire and sample
        # self.ttl4.pulse(15*us) # trigger flash lamp
        # delay(135*us) # wait optimal time (see Minilite manual)
        # self.ttl6.pulse(15*us) # trigger q-switch
        
        with parallel:
            
            with sequential:
                delay(150*us)
                #self.ttl4.pulse(15*us) # trigger flash lamp
                delay(135*us) # wait optimal time (see Minilite manual)
                #self.ttl6.pulse(15*us) # trigger q-switch
                delay(100*us) # wait until some time after green flash
                self.ttl5.pulse(15*us) # trigger uv ccd
            with sequential:
                for j in range(self.scope_count):
                    self.sampler0.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
                    data0[j] = smp[0]
                    data1[j] = smp[1]
                    data2[j] = smp[2]
                    data3[j] = smp[3]
         #           data4[j] = smp[4]
          #          data5[j] = smp[5]
           #         data6[j] = smp[6]
            #        data7[j] = smp[7]
                    #delay(5*us)
                    delay(50*us) # plus 9us from sample_mu

        
        ### Allocate and Transmit Data
        # index = range(self.scope_count)
        # self.mutate_dataset('absorption',index,data0)
        # self.mutate_dataset('fire_check',index,data1)
        self.set_dataset('absorption',(data0),broadcast=True) # class dataset for Artiq communication
        self.set_dataset('fire_check',(data1),broadcast=True) # class dataset for Artiq communication
        self.set_dataset('pmt',(data2),broadcast=True)
        self.set_dataset('spec_check',(data3),broadcast=True)
        #rename before using...
        #self.set_dataset('TBD1',(data4),broadcast=True)
        #self.set_dataset('TBD2',(data5),broadcast=True)
        #self.set_dataset('TBD3',(data6),broadcast=True)
        #self.set_dataset('TBD4',(data7),broadcast=True)


    def run(self):
        ### Initilizations
        self.core.reset() # Initializes Artiq (required)
        # self.set_dataset('absorption',np.full(self.scope_count,np.nan)) # class dataset for Artiq communication
        # self.set_dataset('fire_check',np.full(self.scope_count,np.nan)) # class dataset for Artiq communication

        set_freqs = [] # absorption signal
        volts = [] # absorption signal
        frchks = [] # yag fire check
        fluor = [] # fluorescence pmt signal
        postsel = [] # spec post select
        avgs = [0]*self.setpoint_count
        self.set_dataset('spectrum',(avgs),broadcast=True)
        
        #scan_count = 9 # number of loops/averages
        #scan_offset = 383.949702 # THz
        #no_of_points = 100
        slow_filename = '/home/molecules/skynet/Logs/setpoint2.txt'
        slow_file = open(slow_filename,'w')
        slow_file.write(str(self.slowing_set))
        slow_file.close()

        # Define scan parameters
        scan_interval = 0.5 * np.linspace(self.setpoint_min,self.setpoint_max,self.setpoint_count) * 1.0e6 # MHz
        scan_interval = self.setpoint_offset + scan_interval/1e12
  
        # End of define scan parameters



        my_today = datetime.datetime.today()

        datafolder = '/home/molecules/software/Molecules_Artiq_Sequences/artiq-master/results/Tests/'
        setpoint_filename = '/home/molecules/skynet/Logs/setpoint.txt'


        basefolder = str(my_today.strftime('%Y%m%d')) # 20190618
        # create new folder if doesn't exist yet
        if not os.path.exists(datafolder + basefolder):
            os.makedirs(datafolder + basefolder)

        basefilename = datafolder + basefolder + '/' + str(my_today.strftime('%Y%m%d_%H%M%S')) # 20190618_105557

        #save run configuration
        conf_file = open(basefilename+'_conf','w')
        conf_str = basefilename+'\n'
        conf_str += 'Number of Samples per Shot: '+str(self.scope_count)+'\n'
        conf_str += 'Number of Averages: '+str(self.scan_count)+'\n'
        conf_str += 'Number of Setpoints: '+str(self.setpoint_count)+'\n'
        conf_str += 'Setpoint Offset: '+str(self.setpoint_offset)+' THz\n'
        conf_str += 'Setpoint Min: '+str(self.setpoint_min)+' MHz\n'
        conf_str += 'Setpoint Max: '+str(self.setpoint_max)+' MHz\n'
        conf_str += 'Slowing Frequency: '+str(self.slowing_set)+' THz\n'
        conf_file.write(conf_str)
        conf_file.close()
        print('Config File Written')

        for n, nu in enumerate(scan_interval): 
            print('-'*30)
            print('Setpoint {}/{}'.format(n+1,self.setpoint_count))
            print('Setting laser to ' + str(nu))

            # move laser to set point
            setpoint_file = open(setpoint_filename, 'w')
            setpoint_file.write(str(nu))
            setpoint_file.close()

            new_avg = 0

            time.sleep(1.5)
            

            # run scan_count averages
        
            ### Run Experiment
            for i in range(self.scan_count):
                self.scheduler.pause()
                shot_fired = False
                blue_on = False

                while not shot_fired and not blue_on:
                    #break  #break will break out of the infinite while loop
    #                input('Press ENTER for Run {}/{}'.format(i+1,scan_count))
                    self.fire_and_read() # fires yag and reads voltages
                    vals = self.get_dataset('absorption')
                    chks = self.get_dataset('fire_check')
                    pmts = self.get_dataset('pmt')
                    psel = self.get_dataset('spec_check')

                    hlp = []
                    for v in vals:
                        hlp.append(splr.adc_mu_to_volt(v))

                    hlp2 = []
                    for f in chks:
                        hlp2.append(splr.adc_mu_to_volt(f))

                    hlp3 = []
                    for p in pmts:
                        hlp3.append(splr.adc_mu_to_volt(p))

                    hlp4 = []
                    for ps in psel:
                        hlp4.append(splr.adc_mu_to_volt(ps))

                    # check if Yag fired
                    if np.max(np.array(hlp2)) > 0: ## NORMALLY 0.5 in actual run
                        # save set points for each shot
                        if np.min(np.array(hlp4)) < 0: ## NORMALLY > 0.5 in actual run
                            set_freqs.append(nu)
                            volts.append(hlp)
                            frchks.append(hlp2)
                            fluor.append(hlp3)
                            postsel.append(hlp4)
                            new_avg = new_avg + sum(hlp[20:40])
        
                            print('Run {}/{} Completed'.format(i+1,self.scan_count))
                            shot_fired = True
                            blue_on = True
                        else:
                            blue_on = False
                            print('Repeat shot. No Blue.')
                    else:
                        #break
                        # repeat shot
                        shot_fired = True ### Normally false in actual run
                        print('Repeat shot. No Yag.')
                
                    time.sleep(1)

            new_avg = new_avg/self.scan_count
            self.mutate_dataset('spectrum',n,new_avg)


        # transform into numpy arrays                
        freqs = np.array(set_freqs)
        ch1 = np.array(volts)
        ch2 = np.array(frchks)
        ch3 = np.array(fluor)
        ch4 = np.array(postsel)

        #print(freqs)

        print('Saving data ...')
        ### Write Data to Files
        f_freqs = open(basefilename + '_freqs','w')
        f_ch1 = open(basefilename + '_ch1','w')
        f_ch2 = open(basefilename + '_ch2','w')
        f_ch3 = open(basefilename + '_ch3','w')
        f_ch4 = open(basefilename + '_ch4','w')

        np.savetxt(f_freqs, freqs, delimiter=",")
        f_freqs.close()

        np.savetxt(f_ch1, ch1, delimiter=",")
        f_ch1.close()

        np.savetxt(f_ch2, ch2, delimiter=",")
        f_ch2.close()

        np.savetxt(f_ch3, ch3, delimiter=",")
        f_ch3.close()

        np.savetxt(f_ch4, ch4, delimiter=",")
        f_ch4.close()

        print('Filename: ' + basefilename)

        conf_file = open(basefilename+'_conf','a')
        conf_file.write('RUN FINISHED')
        conf_file.close()

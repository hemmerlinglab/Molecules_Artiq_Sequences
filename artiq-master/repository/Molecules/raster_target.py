# use 'artiq-run' command
from artiq.experiment import *
import artiq.coredevice.sampler as splr
import numpy as np
import datetime
import os
import time
import csv
import socket

from helper_functions import *




# every Experiment needs a build and a run function
class Raster_Target(EnvExperiment):
    def build(self):
        self.setattr_device('core') # Core Artiq Device (required)
        self.setattr_device('ttl4') # flash-lamp
        self.setattr_device('ttl6') # q-switch
        self.setattr_device('ttl5') # uv ccd trigger
        self.setattr_device('sampler0') # adc voltage sampler
        self.setattr_device('scheduler') # scheduler used
        # EnvExperiment attribute: number of voltage samples per scan
        self.setattr_argument('scope_count',NumberValue(default=400,unit='reads per shot',scale=1,ndecimals=0,step=1))
        self.setattr_argument('scan_count',NumberValue(default=1,unit='averages',scale=1,ndecimals=0,step=1))
        self.setattr_argument('step_size',NumberValue(default=60,unit='us',scale=1,ndecimals=0,step=1))

        # x
        self.setattr_argument('min_x',NumberValue(default=3.5,unit='',scale=1,ndecimals=3,step=0.001))
        self.setattr_argument('max_x',NumberValue(default=4.6,unit='',scale=1,ndecimals=3,step=0.001))
        self.setattr_argument('steps_x',NumberValue(default=3,unit='',scale=1,ndecimals=1,step=1))
        
        # y
        self.setattr_argument('min_y',NumberValue(default=3.25,unit='',scale=1,ndecimals=3,step=0.001))
        self.setattr_argument('max_y',NumberValue(default=5.50,unit='',scale=1,ndecimals=3,step=0.001))
        self.setattr_argument('steps_y',NumberValue(default=3,unit='',scale=1,ndecimals=1,step=1))

        ## set circle
        #self.setattr_argument('radius',NumberValue(default=0.0,unit='',scale=1,ndecimals=3,step=0.001))
        #self.setattr_argument('x',NumberValue(default=0.0,unit='',scale=1,ndecimals=3,step=0.001))
        #self.setattr_argument('y',NumberValue(default=0.0,unit='',scale=1,ndecimals=3,step=0.001))

        self.setattr_argument('pmt_slice_min',NumberValue(default=5,unit='ms',scale=1,ndecimals=1,step=0.1))
        self.setattr_argument('pmt_slice_max',NumberValue(default=6,unit='ms',scale=1,ndecimals=1,step=0.1))
        self.setattr_argument('slice_min',NumberValue(default=5,unit='ms',scale=1,ndecimals=1,step=0.1))
        self.setattr_argument('slice_max',NumberValue(default=6,unit='ms',scale=1,ndecimals=1,step=0.1))
        
        self.setattr_argument('yag_power',NumberValue(default=5,unit='',scale=1,ndecimals=1,step=0.1))
        self.setattr_argument('he_flow',NumberValue(default=3,unit='sccm',scale=1,ndecimals=1,step=0.1))
        
        self.setattr_argument('yag_check',BooleanValue())
        self.setattr_argument('blue_check',BooleanValue())

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
        
        delay(260*us)
        
        ### Data Variable Initialization
        data0 = [0]*self.scope_count # signal data
        data1 = [0]*self.scope_count # fire check data
        data2 = [0]*self.scope_count # uhv data
        data3 = [0]*self.scope_count # post select, checks spec blue
        data4 = [0]*self.scope_count # post select, checks slow blue
        smp = [0]*8 # individual sample

        ### Fire and sample
        # self.ttl4.pulse(15*us) # trigger flash lamp
        # delay(135*us) # wait optimal time (see Minilite manual)
        # self.ttl6.pulse(15*us) # trigger q-switch
        
        with parallel:
            
            with sequential:
                delay(150*us)
                self.ttl4.pulse(15*us) # trigger flash lamp
                delay(135*us) # wait optimal time (see Minilite manual)
                self.ttl6.pulse(15*us) # trigger q-switch
                delay(100*us) # wait until some time after green flash
                self.ttl5.pulse(15*us) # trigger uv ccd
            with sequential:
                for j in range(self.scope_count):
                    self.sampler0.sample_mu(smp) # (machine units) reads 8 channel voltages into smp
                    data0[j] = smp[0]
                    data1[j] = smp[1]
                    data2[j] = smp[2]
                    data3[j] = smp[3]
                    data4[j] = smp[4]
                    #delay(5*us)
                    delay(self.step_size*us) # plus 9us from sample_mu

        
        ### Allocate and Transmit Data
        # index = range(self.scope_count)
        # self.mutate_dataset('absorption',index,data0)
        # self.mutate_dataset('fire_check',index,data1)
        self.set_dataset('absorption',(data0),broadcast=True) # class dataset for Artiq communication
        self.set_dataset('fire_check',(data1),broadcast=True) # class dataset for Artiq communication
        self.set_dataset('pmt',(data2),broadcast=True)
        self.set_dataset('spec_check',(data3),broadcast=True)
        self.set_dataset('slow_check',(data4),broadcast=True)



    def prepare(self):
        # function is run before the experiment, i.e. before run() is called
        # https://m-labs.hk/artiq/manual/core_language_reference.html#module-artiq.language.environment
        
        my_today = datetime.datetime.today()

        datafolder = '/home/molecules/software/data/'
        setpoint_filename = '/home/molecules/skynet/Logs/setpoint.txt'

        basefolder = str(my_today.strftime('%Y%m%d')) # 20190618
        # create new folder if doesn't exist yet
        if not os.path.exists(datafolder + basefolder):
            os.makedirs(datafolder + basefolder)

        self.basefilename = datafolder + basefolder + '/' + str(my_today.strftime('%Y%m%d_%H%M%S')) # 20190618_105557

        # how can we get all arguments?
        #save run configuration
        self.config_dict = [
                {'par' : 'scope_count', 'val' : self.scope_count, 'cmt' : 'Number of samples per shot'},
                {'par' : 'scan_count', 'val' : self.scan_count, 'cmt' : 'Number of averages'},
                {'par' : 'step_size', 'val' : self.step_size, 'cmt' : 'Step size'},
                {'par' : 'he_flow', 'val' : self.he_flow, 'unit' : 'sccm', 'cmt' : 'He flow'},
                {'par' : 'yag_power', 'val' : self.yag_power, 'cmt' : 'He flow'},
                {'par' : 'min_x', 'val' : self.min_x, 'cmt' : 'min x'},
                {'par' : 'min_y', 'val' : self.min_y, 'cmt' : 'min y'},
                {'par' : 'max_x', 'val' : self.max_x, 'cmt' : 'max x'},
                {'par' : 'max_y', 'val' : self.max_y, 'cmt' : 'max y'},
                {'par' : 'steps_x', 'val' : self.steps_x, 'cmt' : 'steps x'},
                {'par' : 'steps_y', 'val' : self.steps_y, 'cmt' : 'steps y'},
                {'par' : 'yag_power', 'val' : self.yag_power, 'cmt' : 'He flow'},
                {'par' : 'yag_check', 'val' : self.yag_check, 'cmt' : 'Yag check'},
                {'par' : 'blue_check', 'val' : self.blue_check, 'cmt' : 'Blue check'},
                ]

        save_config(self.basefilename, self.config_dict)

        for k in range(5):
            print("")
        print("*"*100)
        print("* Starting new scan")
        print("*"*100)
        print("")
        print("")

        print('Filename: ' + self.basefilename)


    def analyze(self):
        # function is run after the experiment, i.e. after run() is called
        # save data
        print('Saving data ...')
        save_all_data(self.basefilename,
                [{'var' : self.set_pos_x, 'name' :'setx'},
                 {'var' : self.set_pos_y, 'name' :'sety'},
                 {'var' : self.volts, 'name' :'ch1'},
                 {'var' : self.fluor, 'name' :'ch3'}
                 ])

        # overwrite config file with complete configuration
        self.config_dict.append({'par' : 'Status', 'val' : True, 'cmt' : 'Run finished.'})
        save_config(self.basefilename, self.config_dict)

        print('Scan ' + self.basefilename + ' finished.')


    def run(self):
        ### Initilizations
        self.core.reset() # Initializes Artiq (required)
        # self.set_dataset('absorption',np.full(self.scope_count,np.nan)) # class dataset for Artiq communication
        # self.set_dataset('fire_check',np.full(self.scope_count,np.nan)) # class dataset for Artiq communication

        self.scan_x_interval = np.linspace(self.min_x, self.max_x, self.steps_x)
        self.scan_y_interval = np.linspace(self.min_y, self.max_y, self.steps_y)

        self.setpoint_count = len(self.scan_x_interval) * len(self.scan_y_interval)

        self.set_pos_x  = [] # x pos
        self.set_pos_y  = [] # y pos

        self.volts = [] # absorption signal
        #frchks = [] # yag fire check
        self.fluor = [] # fluorescence pmt signal
        #postsel = [] # spec blue post select
        #postsel2 = [] # slow blue post select
        avgs = [0]*self.setpoint_count
        pmt_avgs = [0]*self.setpoint_count
        
        target_img_incell = [[0] * len(self.scan_y_interval)] * len(self.scan_x_interval) 
        target_img_fluo = [[0] * len(self.scan_y_interval)] * len(self.scan_x_interval) 

        target_img_incell = np.array(target_img_incell, dtype = np.float)
        target_img_fluo = np.array(target_img_fluo, dtype = np.float)

        self.set_dataset('target_img_incell',(target_img_incell),broadcast=True)
        self.set_dataset('target_img_fluo',(target_img_fluo),broadcast=True)
        self.set_dataset('spectrum',(avgs),broadcast=True)
        self.set_dataset('pmt_spectrum',(pmt_avgs),broadcast=True)
        
        # Define scan parameters
        (mesh_X, mesh_Y) = np.meshgrid(self.scan_x_interval, self.scan_y_interval)
        mesh_X = mesh_X.flatten()
        mesh_Y = mesh_Y.flatten()

        self.set_dataset('position_x',(mesh_X),broadcast=True)
        self.set_dataset('position_y',(mesh_Y),broadcast=True)

        self.set_dataset('times',(np.linspace(0,(self.step_size+9)*(self.scope_count-1)/1e3,self.scope_count)),broadcast=True)
        # End of define scan parameters


       
        for nx, xpos in enumerate(self.scan_x_interval): 
            for ny, ypos in enumerate(self.scan_y_interval): 

                print('Setting x/y position to ' + str(xpos) + '/' + str(ypos))

                # move mirrors
                # init connection to python server to send commands to move mirrors
                # Create a TCP/IP socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = ('192.168.42.20', 62000)
                print('connecting to %s port %s' % server_address)
                sock.connect(server_address)

                message = "{0:5.3f}/{1:5.3f}".format(xpos, ypos)
                print('Moving mirrors ... ' + message)
                
                print('Sending message ...')
                sock.sendall(message.encode())                
                print('Done sending ...')
               
                # allow for some time at the edges
                if (ny == 0):
                    print('Sleeping for 7 ...')
                    time.sleep(7)
                else:
                    print('Sleeping for 1 ...')
                    time.sleep(1)

                sock.close()
                print('Socket closed ...')

                new_avg = 0
                new_avg_pmt = 0
                
                new_avg_pic = 0


                # run scan_count averages
        
                ### Run Experiment
                for i in range(self.scan_count):
                    self.scheduler.pause()
                    shot_fired = False
                    blue_on = False # spec
                    slow_on = False # slowing

                    while not shot_fired and not blue_on:
                        #break  #break will break out of the infinite while loop
    #                    input('Press ENTER for Run {}/{}'.format(i+1,scan_count))
                        self.fire_and_read() # fires yag and reads voltages
                        vals = self.get_dataset('absorption')
                        chks = self.get_dataset('fire_check')
                        pmts = self.get_dataset('pmt')
                        psel = self.get_dataset('spec_check')
                        psel2 = self.get_dataset('slow_check')

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

                        hlp5 = []
                        for ps2 in psel:
                            hlp5.append(splr.adc_mu_to_volt(ps2))
                        
                        blue_min = splr.adc_mu_to_volt(40)
                        slow_min = splr.adc_mu_to_volt(40)


                        if self.yag_check:
                            yag_min = 0.3
                        else:
                            yag_min = 0.0

                        # check if Yag fired
                        if np.max(np.array(hlp2)) > yag_min: # 0.3:
                            # save set points for each shot
                            if not self.blue_check:
                                blue_min = 0.0

                            if np.min(np.array(hlp4)) > blue_min:
                                self.set_pos_x.append(xpos)
                                self.set_pos_y.append(ypos)

                                self.volts.append(hlp)
                                #frchks.append(hlp2)
                                self.fluor.append(hlp3)

                                #postsel.append(hlp4)
                                #postsel2.append(hlp5)
                                
                                new_avg = new_avg + sum(hlp[int(self.slice_min*1e3/self.step_size):int(self.slice_max*1e3/self.step_size)])                                    
                                new_avg_pmt = new_avg_pmt + sum(hlp3[int(self.pmt_slice_min*1e3/self.step_size):int(self.pmt_slice_max*1e3/self.step_size)])

                                # integrate over in-cell signal after normalizing with the last <offset_pnts> number of points
                                offset_pnts = 10
                                new_avg_pic = new_avg_pic + np.sum(hlp[int(self.slice_min*1e3/self.step_size):int(self.slice_max*1e3/self.step_size)] - np.mean(hlp[-offset_pnts:]))

                                print('Scan {}/{} Completed'.format(i+1,self.scan_count))
                                shot_fired = True
                                blue_on = True
                                slow_on = True
                            else:
                                blue_on = False
                                print('Repeat shot. No Spec Blue.')
                        else:
                            #break
                            # repeat shot
                            shot_fired = False
                            print('Repeat shot. No Yag.')
                    
                        #time.sleep(1)

                lin_ind = nx*len(self.scan_y_interval) + ny
                #slice_ind = ((nx,nx+1), (ny,ny+1))
                slice_ind = ((nx,nx+1), (ny,ny+1))
                self.mutate_dataset('spectrum', lin_ind, new_avg)
                self.mutate_dataset('pmt_spectrum', lin_ind, new_avg_pmt)

                self.mutate_dataset('target_img_incell', slice_ind, np.abs(new_avg_pic))
                self.mutate_dataset('target_img_fluo', slice_ind, np.abs(new_avg_pmt))
                
                print()
                print()

                #self.mutate_dataset('target_img_incell', (nx, ny), new_avg)
                #self.mutate_dataset('target_img_fluo', (nx, ny), new_avg_pmt)



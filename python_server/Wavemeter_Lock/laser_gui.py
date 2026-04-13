##################################
# Imports
##################################

import sys
import numpy as np
import scipy
import datetime
import fileinput
import socket

# PyQt imports

from PyQt5.QtWidgets import QLineEdit, QTabWidget, QSizePolicy, QTextEdit, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QSpinBox,QVBoxLayout,QPushButton,QLabel,QHBoxLayout,QRadioButton,QButtonGroup,QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer

from matplotlib.backends.qt_compat import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from scipy.interpolate  import interp1d
from functools          import partial
from matplotlib.figure  import Figure


from wavemeter_fiber_switch_server import switch_fiber_channel

###################################

class App(QWidget):
 
    #########################################
    
    def __init__(self):

        self.debug_mode = False

        super().__init__()
        self.title = 'Laser Lock'
        
        # geometry
        self.left       = 0
        self.top        = 0
        self.width      = 200
        self.height     = 500
        self.no_of_rows = 20
        self.set_point  = 0

        self.no_of_points = 100

        self.laser_set_points   = {}
        self.laser_pids_status  = {}
        
        # auto toggle lasers for sample and hold lock
        self.current_laser = 0 # index of channels_to_toggle_lasers
        self.channels_to_toggle_lasers = [1]

        self.initUI()        

        return


    #########################################

    def initUI(self):
             
        self.opts = {
                'fiber_server_ip' : '192.168.42.20',
                'fiber_server_port' : 65000,
                'lasers' : [
                {'id' : 'Davos',    'init_freq' : '384.228000', 'channel' : 1, 'step_size' : '100'},
                {'id' : 'Hodor',    'init_freq' : '389.484000', 'channel' : 2, 'step_size' : '100'},
		        {'id' : 'Daenerys', 'init_freq' : '286.582833', 'channel' : 3, 'step_size' : '100'},
                    ]
                }

        # setpoint server
        self.setpoint_server_addr = '192.168.42.20'
        self.setpoint_server_port = 63700

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.layout = QVBoxLayout()
        
        # add fiber switcher
        hbox_fiber_switcher = self.init_switcherUI()
        self.layout.addLayout(hbox_fiber_switcher) 
        
        # add lasers
        hbox_lasers = self.init_laserUI()
        self.layout.addLayout(hbox_lasers) 
        
        self.setLayout(self.layout) 
        	
        self.show()

    
    #########################################

    def init_laserUI(self):

        hbox = QHBoxLayout()
        
        for k in range(len(self.opts['lasers'])):

            laser = self.opts['lasers'][k]

            single_step = QLineEdit(laser['step_size'])

            set_point = QLineEdit(laser['init_freq'])
            set_point.setReadOnly(True)

            laser_scan = QSpinBox()
            laser_offset = QLineEdit(laser['init_freq'])

            vbox = QVBoxLayout()
            
            hlp = QHBoxLayout()
            hlp.addWidget(QLabel(str(laser['id'])))
            #hlp.addWidget(QLabel('Channel: ' + str(laser['channel'])))
            #hlp.addWidget(QLabel('PID on?'))
            
            #self.laser_pids_status[str(laser['channel'])] = QCheckBox()

            #hlp.addWidget(self.laser_pids_status[str(laser['channel'])])

            vbox.addLayout(hlp)


            vbox.addWidget(QLabel('Frequency Offset (THz)'))        
            vbox.addWidget(laser_offset)
            
            vbox.addWidget(QLabel('Frequency Shift (MHz)'))
            vbox.addWidget(laser_scan)
            
            vbox.addWidget(QLabel('Step Size (MHz)'))               
            vbox.addWidget(single_step)
            
            vbox.addWidget(QLabel('Frequency Set Point (THz)'))
            vbox.addWidget(set_point)

            self.laser_set_points[str(laser['channel'])] = set_point
       
            # define actions
            laser_scan.valueChanged.connect(partial(self.single_step_update, single_step))
            laser_scan.valueChanged.connect(partial(self.set_point_update, laser['channel'], set_point, laser_offset, laser_scan))
            

            # properties
            laser_scan.setSuffix(' MHz')
            laser_scan.setMinimum(-100000)
            laser_scan.setMaximum(100000)
            laser_scan.setSingleStep(int(single_step.text()))

            hbox.addLayout(vbox)

        return hbox
    
    
    #########################################

    def init_switcherUI(self, no_of_switcher_channels = 8):
       
        # Make widget for fiber switcher
        btn = []
       
        self.switcher_group = QButtonGroup()
       
        hbox = QHBoxLayout()

        hbox.addWidget(QLabel('Fiber Switcher'))

        for k in range(no_of_switcher_channels):
            btn = QRadioButton(str(k+1))
            btn.toggled.connect(self.update_switcher)
                                                                            
            if k == 0:
                btn.toggle()
                                                                            
            self.switcher_group.addButton(btn)
                                                                            
            hbox.addWidget(btn)
                                                                            
        return hbox
                                                                            
                                                                            
    #########################################
    
    def update_switcher(self, _):
                                                                            
       btn = self.sender()
       
       if btn.isChecked() and not self.debug_mode:
       
           print('Switching fiber switch to channel ...' + str(btn.text()))
           
           switch_fiber_channel(self.opts, int(btn.text()), wait_time = None, manual_switch = True)

       return

    
    #########################################

    def single_step_update(self, single_step):
        
        btn = self.sender()
        
        btn.setSingleStep(int(single_step.text()))

        return

    
    #########################################
    
    def send_message_via_socket(self, message, addr, port):

        if self.debug_mode:
            print('DEBUG: Sending ... ' + str(message))
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (addr, port)

        sock.connect(server_address)

        sock.sendall(message.encode())

        sock.close()

        return

    
    #########################################
    
    def send_setpoint(self, channel, frequency, do_switch = False, wait_time = 0):

        if do_switch:
            switch = 1
        else:
            switch = 0        
       
        message = "{0:1d},{1:.9f},{2:1d},{3:3d}".format(int(channel), float(frequency), int(switch), int(wait_time))
        #if self.debug_mode:
        #    print(message)

        print('Sending new setpoint for channel {1}: {0:.6f}'.format(frequency, channel))
        self.send_message_via_socket(message, self.setpoint_server_addr, self.setpoint_server_port)

        return

    
    #########################################
    
    def set_point_update(self, which_channel, set_point, laser_offset, laser_scan):
        
        new_set_point = float(laser_offset.text()) + float(laser_scan.value())*1e-6
        
        # update set point
        self.send_setpoint(which_channel, new_set_point, do_switch = False)

        set_point.setText(str(new_set_point))

        return


#########################################
# Main
#########################################

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


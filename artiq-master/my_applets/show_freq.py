#!/usr/bin/env python3

import numpy as np
import PyQt5  # make sure pyqtgraph imports Qt5
# import pyqtgraph
from PyQt5.QtWidgets import QWidget,QLabel,QGridLayout

from artiq.applets.simple import SimpleApplet

class myfreqDisplay(QWidget):
    def __init__(self,args):
        QWidget.__init__(self)
        self.args=args
        layout = QGridLayout()
        self.lab11 = QLabel('Set Point:')
        self.lab12 = QLabel('Act Freq:')
        self.lab21 = QLabel('Set Point:')
        self.lab22 = QLabel('Act Freq:')
        self.lab10 = QLabel('DAVOS:')
        self.lab20 = QLabel('HODOR:')
        layout.addWidget(self.lab10,0,0)
        layout.addWidget(self.lab11,0,1)
        layout.addWidget(self.lab12,0,2)
        layout.addWidget(self.lab20,1,0)
        layout.addWidget(self.lab21,1,1)
        layout.addWidget(self.lab22,1,2)
        self.setLayout(layout)

    def data_changed(self,data,mods):
        try:
            y1 = data[self.args.y1][1]
            offset1 = data[self.args.offset1][1]
            offset2 = data[self.args.offset2][1]
            lnum = data[self.args.lnum][1]
            y2 = data[self.args.y2][1]
        except KeyError:
            return

        # x = data.get(self.args.x, (False, None))[1]
        # if x is None:
            # x = np.zeros(len(y))

        try:
            # print(np.nonzero(y1)[0][-1])
            newy1 = y1[np.nonzero(y1)[0][-1]]*1e-6   
        except:
            newy1 = y1[0]*1e-6
            # print('y1 failed...')

        try:
            newy2 = y2[np.nonzero(y2)[0][-1]][0]
        except:
            newy2 = y2[0]

        if lnum == 1:
            new11 = '{:.6f} THz'.format(offset1+newy1)
            if newy2 > 900:
                new12 = 'CHECK WAVEMETER'
            else:
                new12 = '{:.6f} THz'.format(newy2)
            new21 = '{:.6f} THz'.format(offset2)
            new22 = 'NOT SCANNING'
        elif lnum == 2:
            new11 = '{:.6f} THz'.format(offset1)
            new12 = 'NOT SCANNING'
            new21 = '{:.6f} THz'.format(offset2+newy1)
            if newy2 > 900:
                new22 = 'CHECK WAVEMETER'
            else:
                new22 = '{:.6f} THz'.format(newy2)
        else:
            print("BAD LNUM")
    
        self.lab11.setText('Set Point: {}'.format(new11))
        self.lab12.setText('Act Freq: {}'.format(new12))
        self.lab21.setText('Set Point: {}'.format(new21))
        self.lab22.setText('Act Freq: {}'.format(new22))
            # print('y2 failed...')
            # return


# class myspecXYPlot(pyqtgraph.PlotWidget):
#     def __init__(self, args):
#         pyqtgraph.PlotWidget.__init__(self)
#         self.args = args

#     def data_changed(self, data, mods, title):
#         try:
#             y1 = data[self.args.y][1]
#             y2 = data[self.args.y][2]
#         except KeyError:
#             return

#         x = data.get(self.args.x, (False, None))[1]
#         if x is None:
#             x = np.arange(len(y))
   
#         self.clear()
#         #self.plot(x, y, pen=None, symbol="x")
#         #self.plot(x, y, pen='r', symbol="o")#pen=None, symbol="x")
#         self.plot(x, y2 - y1, pen='r')
#         self.setTitle(title)
#         self.setLabel('bottom', 'Frequency (MHz)')


def main():
    applet = SimpleApplet(myfreqDisplay)
    # applet.argparser.add_argument("--offset",type=float,default=0.0,help="frequency offset")
    applet.add_dataset("y1", "Y values")
    applet.add_dataset("y2", "Y2 values")
    applet.add_dataset("offset1","freq1 offset")
    applet.add_dataset("offset2","freq2 offset")
    applet.add_dataset("lnum","which scanning laser")
    applet.add_dataset("x", "X values", required=False)

    applet.run()

if __name__ == "__main__":
    main()

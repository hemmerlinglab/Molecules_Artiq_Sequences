#!/usr/bin/env python3

import numpy as np
import PyQt5  # make sure pyqtgraph imports Qt5
import pyqtgraph

from artiq.applets.simple import TitleApplet


class myXYPlot(pyqtgraph.PlotWidget):
    def __init__(self, args):
        pyqtgraph.PlotWidget.__init__(self)
        self.args = args

        # self.setXRange(0,28*2)
        # self.setYRange(0,3000)

    def data_changed(self, data, mods, title):
        try:
            y = data[self.args.y][1]
        except KeyError:
            return

        x = data.get(self.args.x, (False, None))[1]
        if x is None:
            x = np.arange(len(y))
   
        self.clear()
        #self.plot(x, y, pen=None, symbol="x")
        #self.plot(x, y, pen='r', symbol="o")#pen=None, symbol="x")
        self.plot(x, y, pen='r')#pen=None, symbol="x")
        self.setTitle(title)
        self.setLabel('bottom', 'Time (ms)') 


def main():
    applet = TitleApplet(myXYPlot)
    applet.add_dataset("y", "Y values")
    applet.add_dataset("x", "X values", required=False)
    applet.run()

if __name__ == "__main__":
    main()

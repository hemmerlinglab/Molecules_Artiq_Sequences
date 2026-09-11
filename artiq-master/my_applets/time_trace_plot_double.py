#!/usr/bin/env python3

import numpy as np
import PyQt5  # make sure pyqtgraph imports Qt5
import pyqtgraph

from artiq.applets.simple import TitleApplet


class my_time_trace_plot(pyqtgraph.PlotWidget):
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


        # plot the data

        self.clear()

        self.plot(x, y1, 
                pen='r', # connecting line color
                )

        self.plot(x, y2, 
                pen='r', # connecting line color
                )


        # Title and labels

        self.setTitle(title)
        self.setLabel('bottom', 'Time (ms)') 


def main():
    applet = TitleApplet(my_time_trace_plot)
    applet.add_dataset("y", "Y values")
    applet.add_dataset("x", "X values", required=False)
    applet.run()

if __name__ == "__main__":
    main()




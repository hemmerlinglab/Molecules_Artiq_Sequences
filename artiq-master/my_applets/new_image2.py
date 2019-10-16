#!/usr/bin/env python3

import PyQt5  # make sure pyqtgraph imports Qt5
import pyqtgraph

from artiq.applets.simple import SimpleApplet

import numpy as np

class NewImage(pyqtgraph.ImageView):
    def __init__(self, args):
        pyqtgraph.ImageView.__init__(self)
        self.args = args

    def data_changed(self, data, mods):
        try:
            img = data[self.args.img][1]
        except KeyError:
            return

        self.setImage(img)

        #pos = np.array([0., 1., 0.5, 0.25, 0.75])
        #color = np.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255], (0, 255, 255, 255), (255, 255, 0, 255)], dtype=np.ubyte)
        #cmap = pg.ColorMap(pos, color)
        
        lut = cmap.getLookupTable(0.0, 1.0, 256)
        self.setLookupTable(lut)

        #hist.gradient.setColorMap(cmap)
        #pl.autoRange()

def main():
    applet = SimpleApplet(NewImage)
    applet.add_dataset("img", "image data (2D numpy array)")
    applet.run()

if __name__ == "__main__":
    main()

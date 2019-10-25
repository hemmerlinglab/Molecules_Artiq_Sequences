#!/usr/bin/env python3

import PyQt5  # make sure pyqtgraph imports Qt5
import pyqtgraph

from artiq.applets.simple import SimpleApplet

import numpy as np

class TargetImage(pyqtgraph.ImageView):
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
        #cmap = pyqtgraph.ColorMap(pos, color)
        #
        #lut = cmap.getLookupTable(0.0, 1.0, 256)
        #img.setLookupTable(lut)
#        colors = [
#    (0, 0, 0),
#    (45, 5, 61),
#    (84, 42, 55),
#    (150, 87, 60),
#    (208, 171, 141),
#    (255, 255, 255)
#]
#
#        #self.setColorMap(pyqtgraph.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors))
#        self.setColorMap(pyqtgraph.ColorMap(pos=(0.0, 1.0), color=colors))

        #hist.gradient.setColorMap(cmap)
        #pl.autoRange()

def main():
    applet = SimpleApplet(TargetImage)
    applet.add_dataset("img", "image data (2D numpy array)")
    applet.run()

if __name__ == "__main__":
    main()

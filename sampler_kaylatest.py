from artiq.experiment import *
from artiq.language.environment.NumberValue import * # is something like this needed??


""" Questions:
    1. What does the build function do in artiq?
    
    Notes:
    2. Run function is what actually gets ran """



class MgmtTutorial(EnvExperiment):
    """Management tutorial"""
    # cannot get the modification in the tutorial to work
    def build(self):
        self.setattr_argument("count", NumberValue(ndecimals=0, step=1))
    
    def run(self):
        for i in range(self.count):
            print("Hello World")

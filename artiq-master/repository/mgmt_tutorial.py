from artiq.experiment import*

class MgmtTutorial(EnvExperiment):
    """Management tutorial"""
    defbuild(self):
        pass # no devices used
    defrun(self):
        print("Hello World")

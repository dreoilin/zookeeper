"""
ZooKeeper
~~~~~~~~~

This is the entry point for the program.

I've just used a script (for now)

SCPI
~~~~~~~~
The SCPI package allows for easy interfacing
with a VISA device
ASRL/dev/ttyUSB0::INSTR
"""
from os import path
import sys
import configparser
import logging
from .drivers.KS33522B import KS33522B
from .drivers.HMP4040 import HMP4040

backend="@py"
configfile="devices.ini"

def main():
    instruments = setup()
    import IPython; IPython.embed()
    
def setup():
    instruments = {}
    basepath = path.dirname(__file__)
    configpath = path.abspath(path.join(basepath, '..', configfile))
    config = configparser.ConfigParser()
    config.read(configpath)
    # import IPython; IPython.embed()
    for key in config.sections():
        dev = config[key]['device']
        port = config[key]['port']
        inst = globals()[dev](port=port)
        instruments[key] = inst
    
    return instruments

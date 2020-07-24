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
import sys
import logging
from . import SCPI

backend="@py"
devices = {
        'PSU' : "PORT" 
        }


def main():
    instruments = setup()
    
    PSU = SCPI.HMP4040(port='ASRL/dev/ttyUSB0::INSTR')
    import IPython; IPython.embed()
    
def setup():
    import pyvisa as visa
    devices = {}
    rm = visa.ResourceManager(backend)
    for port in rm.list_resources():
        inst = SCPI.Instrument(port=port, backend=backend)
        try:
            inst.connect()
            ID = inst.id
            devices[port] = ID
        except:
            logging.debug("Not a valid device")
    return devices
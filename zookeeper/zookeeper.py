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
    print(f"Backend is {backend}")
    instruments = setup()
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
            print("An exception occurred")
    return devices
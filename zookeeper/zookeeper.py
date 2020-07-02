"""
ZooKeeper
~~~~~~~~~

This is the entry point for the program.

I've just used a script (for now)

SCPI
~~~~~~~~
The SCPI package allows for easy interfacing
with a VISA device

"""
import SCPI
import pyvisa as visa
import logging
import sys

# contains the device IDs
DEVICES = ()
backend = '@py'
# setup logger
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) 

# find port from resource manager
PSU = SCPI.Instrument(port='ASRL/dev/ttyUSB0::INSTR', backend=backend)
PSU.connect()
print(PSU.STB())
print(PSU.id)
input()
PSU.disconnect()

def setup_instruments(resource_manager=None):
    
    if resource_manager is None:
        logging.critical("No resource manager specified")
        raise ValueError

    

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
# import pyvisa as visa
import logging
import sys

# contains the device IDs
DEVICES = ()
backend = '@sim'
# setup logger
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) 

# find port from resource manager
PSU = SCPI.Instrument(port='ASRL2::INSTR', backend=backend)
PSU.connect()
print(PSU.MEA.CURR.DC(0))
print(PSU.id)
input()
PSU.disconnect()

def setup_instrument(port, ID=None):
    pass

def main(instruments, command=None):
    pass
    
    

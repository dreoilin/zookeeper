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
from . import SCPI
backend="@py"


def main():
    print(f"BACKEND is {backend}")
    # contains the device IDs
    # DEVICES = ()
    # find port from resource manager
    #PSU = SCPI.Instrument(port='ASRL2::INSTR', backend=backend)
    #PSU.connect()
    #print(PSU.MEA.CURR.DC(0))
    #print(PSU.id)
    #input()
    #PSU.disconnect()    

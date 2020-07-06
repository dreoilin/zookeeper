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
    pass

def setup():
    pass

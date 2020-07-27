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

import sys
import logging
from .Workbench import Workbench

backend="@py"
configfile="devices.ini"

def main():
    mybench = Workbench(configfile)
    import IPython; IPython.embed()
    return mybench
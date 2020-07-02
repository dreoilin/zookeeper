import SCPI
import pyvisa as visa
import logging
import sys

# setup logger
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) 

backend = '@sim'

rm = visa.ResourceManager(backend)

# find port from resource manager
inst = SCPI.Instrument(port='ASRL2::INSTR', backend=backend)
inst.connect()
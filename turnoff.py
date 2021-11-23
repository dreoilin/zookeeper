from zookeeper import main
from time import sleep
import numpy as np
import pandas as pd

# constant of proprtionality for Helmholtz
K = 384.4 # uT/A
H = {
    'start' : 0,
    'stop' : 300
        } # uT
PSU_step = .04 # A
Vptop = 2.5
fexc = 10e3

def setHfield(start=0, stop=100):
    H = {}
    H['start'] = start
    H['stop'] = stop

    return H

def createIs(Istart, Istop, PSU_step):
    return np.arange(Istart, Istop, PSU_step)

H = setHfield(start=0, stop=100) # uT

# connect to zookeeper workbench
# PS, SG, and LIA
wb = main()
wb.connect()

# unpack workbench
PS, WG, LIA = wb.values()
PS.output = 'OFF'
WG.output = 'OFF'
wb.disconnect()

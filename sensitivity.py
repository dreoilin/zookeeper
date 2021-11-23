from zookeeper import main
from time import sleep
import numpy as np
import pandas as pd

# constant of proprtionality for Helmholtz
K = 384.4 # uT/A
H = {
    'start' : 0,
    'stop' : 1000
        } # uT
PSU_step = .02 # A
Vptop = 2.5
fexc = 10e3

def setHfield(start=0, stop=100):
    H = {}
    H['start'] = start
    H['stop'] = stop

    return H

def createIs(Istart, Istop, PSU_step):
    return np.arange(Istart, Istop, PSU_step)

H = setHfield(start=0, stop=1000) # uT

# connect to zookeeper workbench
# PS, SG, and LIA
wb = main()
wb.connect()

# unpack workbench
PS, WG, LIA = wb.values()

Istart = 1/K * H['start']  # A
Istop = 1/K * H['stop'] # A

Is = createIs(Istart, Istop, PSU_step)
V2f = np.zeros(Is.shape)
Imeas = np.zeros(Is.shape)

# setup signal generator
WG.sin(freq = fexc, amp = Vptop, dc = 0)
WG.output = 'ON'

# setup power supply
PS.voltage = 10 # V
# setup LIA
LIA.autosense()
Vptops = np.arange(2.5, 3, 0.1)
freqs = [5e3, 10e3, 15e3, 20e3, 25e3]

for f in freqs:
    fexc = f
    for z, Vptop in enumerate(Vptops):
        WG.sin(freq=fexc, amp=Vptop, dc=0)
        WG.output = 'ON'
        for j, I in enumerate(Is):
            #print(f"Setting PSU current to {I} [A]")
            PS.current = I
            PS.output = 'ON'
            #print(f"PSU output ON")
            sleep(0.2)
            #Imeas[j] = PS.measure(quantity='CURR')
            Imeas[j] = PS.query('MEAS:CURR?')
            #print(f"Multimeter reads {Imeas[j]} [A] from PSU output")
            #print(f"Amplifier autosensing...")
            LIA.autosense()
            #print(f"Waiting 10 seconds for LIA to settle")
            sleep(10)
            #print("Reading V2f from LIA")
            V2f[j] = LIA.query('MAG.')
            #print(f"V2f read as {V2f[j]} [V]")
            sleep(1)

        df = pd.DataFrame({'V2f [V]': V2f, 'Imeas [A]' : Imeas, 'Hfield [uT]' : Imeas * K})

        df.to_csv(f"sine-{Vptop}_Vexc-{fexc}_fexc-to_{H['stop']}uT.csv", index=False)

PS.output = 'OFF'
WG.output = 'OFF'

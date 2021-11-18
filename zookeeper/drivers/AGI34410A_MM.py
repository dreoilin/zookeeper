from .SCPI.VISA_Instrument import VISA_Instrument
import logging
from time import sleep

MEASURE = {
        'VOLTAGE' : ('AC', 'DC'),
        'CAP' : (None),
        'CURR' : ('AC', 'DC'),
        'DIOD' : (None),
        'FREQ' : (None),
        'RES' : (None)
        }


class AGI34410A_MM(VISA_Instrument): 
    def __init__(self, port=None, backend=''):
        super().__init__(port=port, backend=backend, read_termination = '\n', timeout=None)
        logging.info("AGI34410A_MM: Successfully instanciated")
     
    def __repr__(self):
        ret = []
        ret.append("AGI34410A Multimeter")
        ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
        ret.append(super().__repr__()) 
        
        return '\n'.join([r for r in ret])
    
    def __get_attr__(self):
        if attr.upper() in MEASURE.keys():
            def measure(*args):
                return self.SIGNAL(attr.upper(), *args)
            return measure
        
        return super().__getattr__(attr)

    def MEASURE(self, func, *args):
        if len(args) > 0:
            meas = ":" + args.pop().upper()
        else:
            meas = ""
        if meas in MEASURE[func]:
            return self.query(f"MEAS:{func}{meas}?")
        else:
            logging.error("Measurement type {meas} not found.")
            return None

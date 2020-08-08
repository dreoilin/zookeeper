from .SCPI.VISA_Instrument import VISA_Instrument
from .SCPI.SCPI_Instrument import Instrument
import logging
import re

# config = {
#     'id' : None
#     }

SIGNALS = [ # freq, amp, offset
    'SIN', # TODO! fix signal send syntax
    'RAMP', # 100 % symmetry
    'SQUARE',
    'DC',
    'NOISE',
    'PRBS',
    'PULSE',
    'TRIANGLE' # 50% symmetry
    ]

class KS33522B(VISA_Instrument):
    
    def __init__(self, port = None):
        super().__init__(port=port, read_termination='\n')
        logging.info("KS33522B: Successfully instanciated")     
    
    def __repr__(self):
        ret = []
        ret.append(f"KS33522B Signal Generator")
        ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
        ret.append(super().__repr__())
        if self.connected:
            params = ["Function", "Frequency", "Amplitude", "DC Offset"]
            config = re.split(r"[\ \,]", self.apply())
            ret.extend([f"{k} :\t{v}".replace('"', '') for k,v in zip(params, config)])
        
        return '\n'.join([r for r in ret])
        
    def __getattr__(self, attr):
        if attr.upper() in SIGNALS:
            def signal(**kwargs):
                return self.SIGNAL(attr.upper(), **kwargs)
            return signal
        
        return super().__getattr__(attr)
        
    def SIGNAL(self, attr, **kwargs):
        arg = ",".join([str(elem) for elem in
                      [kwargs.get('freq', 'DEF'),
                       kwargs.get('amp', 'DEF'),
                       kwargs.get('dc', 'DEF')]])
        
        
        print(f'APPLY:{attr} {arg}')
        return self.write(f'APPLY:{attr} {arg}')

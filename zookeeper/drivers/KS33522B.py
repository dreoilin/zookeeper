from .SCPI.VISA_Instrument import VISA_Instrument
import logging

config = {
    'id' : None
    }

SIGNALS = [
    'SINE',
    'RAMP'
    ]

class KS33522B(VISA_Instrument):
    
    def __init__(self, port = None):
        super().__init__(port=port, read_termination='\n')
        logging.info("KS33522B: Successfully instanciated")     
    
    def __getattr__(self, attr):
        if attr.upper() in SIGNALS:
            def signal(**kwargs):
                return self.SIGNAL(attr.upper(), **kwargs)
            return signal
        
        super().__getattr__(attr)
        
    def SIGNAL(self, attr, **kwargs):
        # for x in kwargs.items()
        pass
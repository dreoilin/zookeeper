from .SCPI.vxi11_Instrument import vxi11_Instrument
import logging

config = {
    'id' : None
    }

class KS33522B(vxi11_Instrument):
    
    def __init__(self, host = None):
        super().__init__(host=host)
        logging.info("KS33522B: Successfully instanciated")
    
    
from .SCPI.VISA_Instrument import VISA_Instrument
import logging

config = {
    'id' : None
    }

class KS33522B(VISA_Instrument):
    
    def __init__(self, port = None):
        super().__init__(port=port, read_termination='\n')
        logging.info("KS33522B: Successfully instanciated")
        
    
    
    
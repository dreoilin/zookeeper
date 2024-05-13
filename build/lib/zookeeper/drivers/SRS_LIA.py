from .SCPI.VISA_Instrument import VISA_Instrument
import logging

class SRS_LIA(VISA_Instrument):
    def __init__(self, port = None):
        super().__init__(port=port, read_termination='\n')
        logging.info("SRS_LIA: Successfully instanciated")
        
    def __repr__(self):
        ret = []
        ret.append("SRS_LIA Signal Generator")
        ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
        ret.append(super().__repr__())
        if self.connected:
            pass
        
        return '\n'.join([r for r in ret])
   
    def connect(self):
        super().connect()
        logging.info("DSP7265_LIA: connected")
        
    #@property
    #def VMODE(self):
    #    return self.query('VMODE')

    #@VMODE.setter
    #def VMODE(self, mode=1):
    #    """
    #    0 both inputs grounded
    #    1 A input only
    #    2 -B input only
    #    3 A-B differential mode
    #    """
    #    return self.write(f'VMODE {mode}')
    
    @property
    def sensitivity(self):
        return self.query('SENS?')

    @sensitivity.setter
    def sensitivity(self, n=10):
        return self.write(f'SENS {n}')

    def autosense(self):
        """
        Automatically set sensitivity
        """
        return self.write('AGAN')

    #def automeasure(self):
    #    """
    #    Automatically set sensitivity and set phase to minimum
    #    """
    #    return self.write('ASM')
    
    #@property
    #def refchannel(self):
    #    return self.query('IE')

    #@refchannel.setter
    #def refchannel(self, channel=0):
    #    """
    #    0 INT
    #    1 EXT LOGIC
    #    2 EXT (front)
    #    """
    #    return self.write(f'IE {channel}')
    
    def getX(self): 
        return float(self.query('OUTP? 1'))

    def getY(self):
        return float(self.query('OUTP? 2'))

    def getMag(self):
        return float(self.query('OUTP? 3'))
    
    def getPhase(self):
        return float(self.query('OUTP? 5'))

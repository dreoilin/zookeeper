from .SCPI.VISA_Instrument import VISA_Instrument
import logging

class DSP7265_LIA(VISA_Instrument):
    def __init__(self, port = None):
        super().__init__(port=port, read_termination='\r\n')
        logging.info("DSP7265_LIA: Successfully instanciated")
        
    def __repr__(self):
        ret = []
        ret.append("DSP7265_LIA Signal Generator")
        ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
        ret.append(super().__repr__())
        if self.connected:
            pass
        
        return '\n'.join([r for r in ret])
   
    def connect(self):
        super().connect()
        logging.info("DSP7265_LIA: connected")
    
    def id(self):
        return self.query('ID')
        
    @property
    def VMODE(self):
        return self.query('VMODE')

    @VMODE.setter
    def VMODE(self, mode=1):
        """
        0 both inputs grounded
        1 A input only
        2 -B input only
        3 A-B differential mode
        """
        return self.write(f'VMODE {mode}')
    
    @property
    def sensitivity(self):
        return self.query('SEN')

    @sensitivity.setter
    def sensitivity(self, n=24):
        return self.write(f'SEN {n}')

    def autosense(self):
        """
        Automatically set sensitivity
        """
        return self.write('AS')

    def automeasure(self):
        """
        Automatically set sensitivity and set phase to minimum
        """
        return self.write('ASM')
    
    @property
    def refchannel(self):
        return self.query('IE')

    @refchannel.setter
    def refchannel(self, channel=0):
        """
        0 INT
        1 EXT LOGIC
        2 EXT (front)
        """
        return self.write(f'IE {channel}')
    
    def getX(self, volt=False):
        if volt:
            delim = '.'
        else:
            delim = ''
            
        return self.query('X{delim}')

    def getY(self, volt=False):
        if volt:
            delim = '.'
        else:
            delim = ''
            
        return self.query('Y{delim}')

    def getMag(self, volt=False):
        if volt:
            delim = '.'
        else:
            delim = ''
            
        return self.query('MAG{delim}')
    
    def getPhase(self, degrees=True):
        if degrees:
            delim = '.'
        else:
            delim = ''
            
        return self.query('PHA{delim}')





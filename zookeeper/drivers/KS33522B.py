from .SCPI.VISA_Instrument import VISA_Instrument
import logging

config = {
    'id' : None
    }

SIGNALS = [ # freq, amp, offset
    'SINE',
    'RAMP', # 100 % symmetry
    'SQUARE',
    'DC',
    'NOISE',
    'PRBS',
    'PULSE',
    'TRIANGLE' # 50% symmetry
    ]

class SignalArg():
    def __init__(self, **kwargs):
        self.__spec = ('dc', 'amp', 'f')
        self.__command=""
        self.__kwargs = **kwargs
    
    def build_command(self, arg, delim=','):
        self.__command = f"[{delim}{arg}{self.__command}]"
    
    @property
    def command(self):
        for spec in self.__spec:
            for key, value in self.__kwargs:
                # TODO! sort out command building
                # self.build_command(value) if key == spec else sel.build_command('DEF')
                
                
        return self.__command

class KS33522B(VISA_Instrument):
    
    def __init__(self, port = None):
        super().__init__(port=port, read_termination='\n')
        logging.info("KS33522B: Successfully instanciated")     
    
    def __repr__(self):
        pass
    
    def __getattr__(self, attr):
        if attr.upper() in SIGNALS:
            def signal(**kwargs):
                return self.SIGNAL(attr.upper(), **kwargs)
            return signal
        
        super().__getattr__(attr)
        
    def SIGNAL(self, attr, **kwargs):
        arg = ""
        for feature in kwargs.items()
            arg = f"{arg}]"
    
    def _configuration(self):
        return self.apply()
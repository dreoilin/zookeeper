from .SCPI.VISA_Instrument import VISA_Instrument
import logging
from datetime import datetime
import io
import re

SIGNALS = { # freq, amp, offset
    'SIN' : ('Frequency', 'Amplitude', 'DC'),
    'RAMP': ('Frequency', 'Amplitude', 'DC', 'Symmetry'),
    'SQU' : ('Frequency', 'Amplitude', 'DC', 'DCYC'),
    'DC' : ('DC'),
    'NOIS' : ('Bandwidth'),
    'PULS' : ('Frequency', 'Amplitude', 'DC', 'HOLD', 'WIDTH', 'DCYCLE', 'TRANSITION')
    }

#MODULATION = {
#    'AM' : ('Frequency'),
#    'BPSK' : ('Rate'),
#    'FM' : ('Frequency', 'Deviation'),
#    'FSK' : ('Frequency', 'Rate'),
#    'PM' : ('Frequency', 'Deviation'),
#    'PWM' : ('Deviation')
#    }

class AGI33210A_WG(VISA_Instrument):
    def __init__(self, port = None):
        super().__init__(port=port, read_termination='\n')
        logging.info("AGI33210A: Successfully instanciated")
        
    def __repr__(self):
        ret = []
        ret.append("AGI33210A Signal Generator")
        ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
        ret.append(super().__repr__())
        if self.connected:
            setup = []
            params = ["Function", "Frequency", "Amplitude", "DC"]
            setup = re.split(r"[\ \,]", self.apply())
            func = setup[0].replace('"', '')
            ret.extend([f"{k} :\t{v}".replace('"', '') for k,v in zip(params, setup) if k in SIGNALS[func]])
        
        return '\n'.join([r for r in ret])
        
    def __getattr__(self, attr):
        if attr.upper() in SIGNALS.keys():
            def signal(**kwargs):
                return self.SIGNAL(attr.upper(), **kwargs)
            return signal
        
        #if attr.upper() in MODULATION:
        #    def modulation(**kwargs):
        #        return self.MODULATION(attr.upper(), **kwargs)
        #    return modulation
        
        return super().__getattr__(attr)
    
    def SIGNAL(self, func, **kwargs):
        '''
        Magic method to set a signal on the current channel. Signal is not
        pushed to output until output is toggled with `toggle()'
            
        All functions take a frequency, amplitude and dc offset parameter.
        Sevaral other functions are allowed to take extra kwargs like: 
            phase, symmetry etc.
        
        Parameters
        ----------
        attr : STRING
            function name e.g sin, ramp, dc
        **kwargs : VARIABLE
            Variable dictionary of keywords specifying signal params  
        '''
        self.function = func
        self.frequency = kwargs.pop('freq', 'MIN')
        self.amplitude = kwargs.pop('amp', 0)
        self.offset = kwargs.pop('dc', 0)
        if func == "PULS":
            for k, v in kwargs:
                if k in SIGNALS[func]:
                    self.write(f"FUNC:PULS:{k} {v}")
                return

        if 'Symmetry' in SIGNALS[func]:
            self.symmetry = kwargs.pop('sym', 0)
        if 'DCYC' in SIGNALS[func]:
            self.dcycle = kwargs.pop('DCYC', 'MIN')
        
    #def MODULATION(self, modtype, **kwargs):
    #    source = kwargs.get('source', 'INT')
    #    self.write(f"SOUR{self.channel}:{modtype}:SOUR {source}")
    #    if source is 'INT':
    #        if 'Frequency' in MODULATION[modtype]:
    #            freq = kwargs.get('freq', 1e3)
    #            self.write(f"SOUR{self.channel}:{modtype}:INT:FREQ {freq}")     
    #        if modtype is 'AM':
    #            self.DSSC = 'ON' if kwargs.get('DSSC', False) else 'OFF'
    #            # set source function
    #            func = kwargs.get('func', 'SIN').upper()
    #            self.write(f"SOUR{self.channel}:{modtype}:INT:FUNC {func}")
    #            # set mod depth
    #            depth = kwargs.get('depth', 100)
    #            self.write(f"SOUR{self.channel}:{modtype}:DEPT {depth}")
    #        if modtype is 'BPSK':
    #            # set BPSK phase
    #            phase = kwargs.get('phase', 0)
    #            self.write(f"SOUR{self.channel}:{modtype}:PHAS {phase}")
    #        if 'Rate' in MODULATION[modtype]:
    #            # set rate
    #            rate = kwargs.get('rate', 10)
    #            self.write(f"SOUR{self.channel}:{modtype}:INT:RATE {rate}")
    #        if 'Deviation' in MODULATION[modtype]:
    #            # set deviation
    #            dev = kwargs.get('deviation', 10)
    #            self.write(f"SOUR{self.channel}:{modtype}:DEV {dev}")
    #        if modtype is 'PWM':
    #            self.PWMDCYCLE = kwargs.get('dcycle', 1)
    #            
    #    # turn on modulation
    #    state = kwargs.get('state', 'OFF')
    #    return self.write(f"SOUR{self.channel}:{modtype}:STATE {state}")
    
    def connect(self):
        super().connect()
        logging.info("AGI33210A: performing startup procedure")
        self.__startup()
    
    def __startup(self):
        """
        Basic startup routines. Disables the display (provides faster processing
                                                      and basic security)
        """
        selfoutput = 'OFF'
        return
    
    @property
    def dcycle(self):
        return self.query(f'FUNC:SQU:DCYC?')
    
    @dcycle.setter
    def dcycle(self, value):
        return self.write(f'FUNC:SQU:DCYC {value}')
  
    @property
    def frequency(self):
        return float(self.query(f"FREQ?"))
    
    @frequency.setter
    def frequency(self, frequency):
        return self.write(f"FREQ {frequency}")
    
    @property
    def amplitude(self):
        return float(self.query(f"VOLT?"))
    
    @amplitude.setter
    def amplitude(self, amp=2, dc=0):
        self.write(f"VOLT {amp}")
        
    @property
    def offset(self):
        return self.query(f"VOLT:OFFSET?")
    
    @offset.setter
    def offset(self, offset):
        return self.write(f"VOLT:OFFSET {offset}")
    
    @property
    def unit(self):
        return self.query(f"VOLT:UNIT?")

    @unit.setter
    def unit(self, unit='VPP'):
        return self.write(f"VOLT:UNIT {unit}")

    
    @property
    def function(self):
        return self.query(f"FUNC?")
    
    @function.setter
    def function(self, func):
        if func not in SIGNALS:
            raise AttributeError(f"AGI33210A_WG: Signal not supported: {func}")
        
        return self.write(f"FUNC {func}")
    
    @property
    def symmetry(self):
        return self.query(f"FUNC:RAMP:SYMM?")
    
    @symmetry.setter
    def symmetry(self, sym):
        return self.write(f"FUNC:RAMP:SYMM {sym}")
    
   
    @property
    def impedance(self):
        return float(self.query(f"OUTP:LOAD?"))
    
    @impedance.setter
    def impedance(self, value):
        if value not in ['INF', 'MIN', 'MAX'] and not (1 <= value <=10e3):
            raise ValueError(f"Specified output impedance not supported.\nMust be one of INF, MIN, MAX or between 1 and 10k ohms")
        return self.write(f"OUTP:LOAD {value}")
        
    @property
    def output(self):
        return 'ON' if int(self.query(f"OUTP?")) else 'OFF'
    
    @output.setter
    def output(self, key):
        if key not in ['ON', 'OFF']:
            raise ValueError(f'Key >>{key}<< invalid.\nMust be one of ON, OFF')
        return self.write(f"OUTP {key}")
        
    # disconnect procedures
    def disconnect(self):
        self[c].output = 'OFF'
        return super().disconnect()

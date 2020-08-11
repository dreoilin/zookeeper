from .SCPI.VISA_Instrument import VISA_Instrument
import logging
import re

config = {
    'NCHANNELS' : 2
    }

SIGNALS = { # freq, amp, offset
    'SIN' : ['Frequency', 'Amplitude', 'DC', 'Phase'],
    'RAMP': ['Frequency', 'Amplitude', 'DC', 'Phase', 'Symmetry'],
    #'SQUARE' : None,
    'DC' : ['DC'],
    #'NOISE',
    #'PRBS',
    #'PULSE' : None,
    # 'TRIANGLE' : None # 50% symmetry
    }

class KS33522B(VISA_Instrument):
    def __init__(self, port = None):
        super().__init__(port=port, read_termination='\n')
        logging.info("KS33522B: Successfully instanciated")
        self.channel = 1
        
    def __repr__(self):
        ret = []
        ret.append("KS33522B Signal Generator")
        ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
        ret.append(super().__repr__())
        if self.connected:
            setup = []
            for c in [1,2]:
                ret.extend([f"Channel {c}", "~~~~~~~~~~~~"])
                params = ["Function", "Frequency", "Amplitude", "DC"]
                setup = re.split(r"[\ \,]", self.apply())
                func = setup[0].replace('"', '')
                ret.extend([f"{k} :\t{v}".replace('"', '') for k,v in zip(params, setup) if k in SIGNALS[func]])
                ret.extend([f"Phase :\t{self.phase}"])
        
        return '\n'.join([r for r in ret])
        
    def __getattr__(self, attr):
        if attr.upper() in SIGNALS.keys():
            def signal(**kwargs):
                return self.SIGNAL(attr.upper(), **kwargs)
            return signal
        
        return super().__getattr__(attr)
    
    def __getitem__(self, key):
        if key not in range(1, config['NCHANNELS']+1):
            raise ValueError(f"KS33522B supports {config['NCHANNELS']} channels")
        
        self.channel = key
        return self
    
    def SIGNAL(self, attr, **kwargs):
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
        self.function = attr
        self.frequency = kwargs.get('freq', 'MIN')
        self.amplitude = kwargs.get('amp', 0)
        self.offset = kwargs.get('dc', 0)
        if 'phase' in SIGNALS[attr]:
            self.phase = kwargs.get('phase', 0)
        if 'symmetry' in SIGNALS[attr]:
            self.symmmetry = kwargs.get('sym', 0)
        
    def connect(self):
        super().connect()
        logging.info("KS33522B: performing startup procedure")
        self.__startup()
    
    def __startup(self):
        """
        Basic startup routines. Disables the display (provides faster processing
                                                      and basic security)
        """
        self.disp('OFF')
        self.display(msg="Zookeeper: Running tests remotely")
        
    def display(self, msg = None, clear = False):
        """
        Displays a user defined message on the signal generator display

        Parameters
        ----------
        msg : STR
            Message to be displayed on signal generator display
        
        clear : BOOLEAN
            Default : False -> scrubs the display
        
        Returns
        -------
        SUCCESS
            returns a PyVisa success code

        """
        
        if clear is True:
            return self.display.text.clear()
        
        return self.disp.text(f'"{msg}"')
    
    @property
    def channel(self):
        return self.__channel
    
    @channel.setter
    def channel(self, channel : int):
        if not 1 <= channel <= config['NCHANNELS']:
            raise ValueError(f"Specified channel does not exist: {channel}")
            
        self.__channel = channel
        
    # frequency subsystem
    @property
    def frequency(self):
        return float(self.query(f"SOUR{self.channel}:FREQ?"))
    
    @frequency.setter
    def frequency(self, frequency):
        return self.write(f"SOUR{self.channel}:FREQ {frequency}")
    
    
    
    #############################################################
    @property
    def amplitude(self):
        return float(self.query(f"SOUR{self.channel}:VOLT?"))
    
    @amplitude.setter
    def amplitude(self, amp=2, dc=0):
        self.write(f"SOUR{self.channel}:VOLT {amp}")
        
    @property
    def offset(self):
        return self.query(f"SOUR{self.channel}:VOLT:OFFSET?")
    
    @offset.setter
    def offset(self, offset):
        return self.write(f"SOUR{self.channel}:VOLT:OFFSET {offset}")
    
    # Phase subsystem
    @property
    def phase(self):
        return self.query(f"SOUR{self.channel}:PHASE?")
    
    @phase.setter
    def phase(self, phase):
        return self.write(f"SOUR{self.channel}:PHASE {phase}")
    
    def set_phase_ref(self, channel):
        """
        Reset zero phase reference point for specified channel.
        Does not change the waveform
        """
        return self.write(f"SOUR{self.channel}:PHASE:REFERENCE")

    def phase_sync(self):
        '''
        Resets all phase generators, including modulating phase generator,
        to establish a common, internal phase zero reference point.
        '''
        return self.write(f"SOUR{self.channel}:PHASE:SYNC")
    #################################################################
    @property
    def function(self):
        return self.query(f"SOUR{self.channel}:FUNC?")
    
    @function.setter
    def function(self, func):
        if func not in SIGNALS:
            raise AttributeError(f"KS33522B: Signal not supported: {func}")
        
        return self.write(f"SOUR{self.channel}:FUNC {func}")
    
    @property
    def symmetry(self):
        return self.query(f"SOUR{self.channel}:RAMP:SYMM?")
    
    @symmetry.setter
    def symmetry(self, sym):
        return self.write(f"SOUR{self.channel}:RAMP:SYMM {sym}")
    
    # toggle controls
    def toggle(self):
        if self.query(f"OUTP{self.channel}?"):
            return self.write(f"OUTP{self.channel} ON")
        else:
            return self.write(f"OUTP{self.channel} OFF")
    
    # disconnect procedures
    def disconnect(self):
        for c in range(1, config['NCHANNELS']+1):
            self.channel = c
            self.write(f"SOUR{self.channel}:APPLY:DC 0,0,0")
        return super().disconnect()
    
    @property
    def coupled(self):
        return self.query("VOLT:COUP?")
    
    @coupled.setter
    def coupled(self, couple : bool):
        return self.write(f"VOLT:COUP {int(couple)}")
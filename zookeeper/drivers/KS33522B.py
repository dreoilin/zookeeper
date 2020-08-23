from .SCPI.VISA_Instrument import VISA_Instrument
import logging
from PIL import Image
import io
import re

config = {
    'NCHANNELS' : 2
    }

SIGNALS = { # freq, amp, offset
    'SIN' : ['Frequency', 'Amplitude', 'DC', 'Phase'],
    'RAMP': ['Frequency', 'Amplitude', 'DC', 'Phase', 'Symmetry'],
    'SQUARE' : None,
    'DC' : ['DC'],
    'NOISE' : ['Bandwidth'],
    'PRBS' : None,
    'PULSE' : None,
    'TRIANGLE' : None # 50% symmetry
    }

MODULATION = [
    'AM',
    'BPSK',
    'FM',
    'FSK',
    'PM',
    'PWM'
    ]

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
        
        if attr.upper() in MODULATION:
            def modulation(**kwargs):
                return self.MODULATION(attr.upper(), **kwargs)
            return modulation
        
        return super().__getattr__(attr)
    
    def __getitem__(self, key):
        if key not in range(1, config['NCHANNELS']+1):
            raise ValueError(f"KS33522B supports {config['NCHANNELS']} channels")
        
        self.channel = key
        return self
    
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
        self.frequency = kwargs.get('freq', 'MIN')
        self.amplitude = kwargs.get('amp', 0)
        self.offset = kwargs.get('dc', 0)
        if 'Phase' in SIGNALS[func]:
            self.phase = kwargs.get('phase', 0)
        if 'Symmetry' in SIGNALS[func]:
            self.symmetry = kwargs.get('sym', 0)
        if 'Bandwidth' in SIGNALS[func]:
            self.bandwidth = kwargs.get('bandwidth', 'MIN')
        
    def MODULATION(self, modtype, **kwargs):
    
        source = kwargs.get('source', 'INT')
        self.write(f"SOUR{self.channel}:{modtype}:SOUR {source}")
        if source is 'INT':
            if modtype in ['AM', 'FM', 'FSK', 'PM']:
                # set mod frequency
                freq = kwargs.get('freq', 1e3)
                self.write(f"SOUR{self.channel}:{modtype}:INT:FREQ {freq}")
            if modtype is 'AM':
                self.DSSC = 'ON' if kwargs.get('DSSC', False) else 'OFF'
                # set source function
                func = kwargs.get('func', 'SIN').upper()
                self.write(f"SOUR{self.channel}:{modtype}:INT:FUNC {func}")
                # set mod depth
                depth = kwargs.get('depth', 100)
                self.write(f"SOUR{self.channel}:{modtype}:DEPT {depth}")
            if modtype is 'BPSK':
                # set BPSK phase
                phase = kwargs.get('phase', 0)
                self.write(f"SOUR{self.channel}:{modtype}:PHAS {phase}")
            if modtype in ['BPSK', 'FSK']:
                # set rate
                rate = kwargs.get('rate', 10)
                self.write(f"SOUR{self.channel}:{modtype}:INT:RATE {rate}")
            if modtype in ['FM', 'PM', 'PWM']:
                # set deviation
                dev = kwargs.get('deviation', 10)
                self.write(f"SOUR{self.channel}:{modtype}:DEV {dev}")
            if modtype is 'PWM':
                self.PWMDCYCLE = kwargs.get('dcycle', 1)
                
        # turn on modulation
        return self.write(f"SOUR{self.channel}:{modtype}:STATE ON")
        
    def connect(self):
        super().connect()
        logging.info("KS33522B: performing startup procedure")
        self.__startup()
    
    def __startup(self):
        """
        Basic startup routines. Disables the display (provides faster processing
                                                      and basic security)
        """
        for i in [1, 2]:
            self[i].output = 'OFF'
        return
    
    # AM SUBSYSTEM ##############     
    @property
    def DSSC(self):
        """
        Queries amplitude modulation mode - DSSC ('ON') or AM modulated carrier
        with sidebands ('OFF')
        """
        return self.query(f"SOUR{self.channel}:AM:DSSC?")
    
    @DSSC.setter
    def DSSC(self, key):
        if key not in ['ON', 'OFF', 1, 0]:
            raise ValueError(f"Key >>{key}<< not valid. Specify 'ON', 'OFF', 1, 0")
        return self.write(f"SOUR{self.channel}:AM:DSSC {key}")
    
    #############################
    # PWM SUBSYSTEM ############
    @property
    def PWMDCYCLE(self):
        return self.query(f"SOUR{self.channel}PWM:DEV:DCYC?")
    
    @PWMDCYCLE.setter
    def PWMDCYCLE(self, value):
        return self.write(f"SOUR{self.channel}:PWM:DEV:DCYC {value}")
    
    #############################
    def combine(self):
        """
        Combines digital data two channels to create the output
        signal on the output DAC for the base channel
        
        Parameters
        ----------
        channel : int
            target channel to combine with source channel
        """
        return self.write(f"SOUR{self.channel}:COMB:FEED {channel}")
    
    #########################
    # DATA subsystem ########
    
    
    #########################
    
    
    
    @property
    def channel(self):
        return self.__channel
    
    @channel.setter
    def channel(self, channel : int):
        if not 1 <= channel <= config['NCHANNELS']:
            raise ValueError(f"Specified channel does not exist: {channel}")
            
        self.__channel = channel
        
    ################################
    # FREQ subsystem ###############
    
    @property
    def frequency(self):
        return float(self.query(f"SOUR{self.channel}:FREQ?"))
    
    @frequency.setter
    def frequency(self, frequency):
        return self.write(f"SOUR{self.channel}:FREQ {frequency}")
    
    
    
    #################################
    # OSCILLATOR subsystem ##########
    
    @property
    def ROSC(self):
        return self.query(f"ROSC:SOUR?")
    
    @ROSC.setter
    def ROSC(self, key):
        if key.upper() not in ['INT', 'EXT']:
            raise ValueError(f"Key >>{key}<< is invalid.\nSpecify INT or EXT")
        return self.write(f"ROSC:SOUR {key}")
    
    @property
    def autoROSC(self):
        if self.query(f"ROSC:SOUR:AUTO?") is 'ON':
            selected = self.query(f"ROSC:SOUR:CURR?")
            return f"Auto ROSC >> ON\nCH {selected}"
        else:
            return f"Auto ROSC >> OFF"
    
    @autoROSC.setter
    def autoROSC(self, key):
        if key.upper() not in ['ON', 'OFF']:
            raise ValueError(f"Illegal key:\nSpecify ON or OFF")
        return self.write(f"ROSC:SOUR:AUTO {key}")
    ################################
    # SUM subsystem ################
    
    def summation(self, source='EXT', amplitude=0.1):
        if source not in ['CH1', 'CH2', 'EXT']:
            raise ValueError(f"Specified source >>{source}<< is not valid.\nMust be one of CH1, CH2 or EXT")
        self.sumstate = 'OFF'
        # set the sum source
        self.write(f"SOUR{self.channel}:SUM:SOUR {source}")
        # set internal sum modulation depth
        self.write(f"SOUR{self.channel}:SUM:AMPL {amplitude}") if amplitude != 0.1 else None
        self.sumstate = 'ON'
        
        return 
    
    @property
    def sumstate(self):
        return self.query(f"SOUR{self.channel}:SUM:STAT?")
    
    @sumstate.setter
    def sumstate(self, key):
        if key not in ['ON', 'OFF', 1, 0]:
            raise ValueError(f"Key >>{key}<< is invalid.\nMust be one of ON, OFF, 1, 0")
        return self.write(f"SOUR{self.channel}:SUM:STAT {key}")
    ################################
    # TRACK subsystem
    
    def track(self, key):
        if key not in ['ON', 'OFF', 'INV']:
            raise ValueError(f"Key >>{key}<< invalid.\nMust be one of ON, OFF, INV")
        
        return self.write(f"SOUR{self.channel}:TRAC {key}")
    
    ################################
    # TRIGGER subsystem ############
    
    #def trigger(self, )
    ################################
    
    ################################
    # UNIT subsystem
    @property
    def angle(self):
        return self.query(f"UNIT:ANGL?")
    
    @angle.setter
    def angle(self, unit):
        if unit.upper() not in ['DEG', 'RAD']:
            raise ValueError(f"Unit >>{unit}<< invalid.\nMust be one of DEG, RAD")
        return self.write(f"UNIT:ANGLE {unit.upper()}")
    ################################
    @property
    def coupled(self):
        return self.query("VOLT:COUP?")
    
    @coupled.setter
    def coupled(self, couple : bool):
        return self.write(f"VOLT:COUP {int(couple)}")
    
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
        return float(self.query(f"SOUR{self.channel}:PHASE?"))
    
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
        return self.query(f"SOUR{self.channel}:FUNC:RAMP:SYMM?")
    
    @symmetry.setter
    def symmetry(self, sym):
        return self.write(f"SOUR{self.channel}:FUNC:RAMP:SYMM {sym}")
    
    @property
    def bandwidth(self):
        return self.query(f"SOUR{self.channel}:FUNC:NOIS:BAND?")
    
    @bandwidth.setter
    def bandwidth(self, value):
        if not in ['MIN', 'MAX'] and not 1e-3 <= value <= 3e7:
            raise ValueError(f"Noise bandwidth >>{value}<< not supported\nMust be between 1e-3 and 3e7 or one of MIN, MAX")
        return self.write(f"SOUR{self.channel}:FUNC:NOIS:BAND {value}")
    
    @property
    def impedance(self):
        return float(self.query(f"OUTP{self.channel}:LOAD?"))
    
    @impedance.setter
    def impedance(self, value):
        if value not in ['INF', 'MIN', 'MAX'] and not (1 <= value <=10e3):
            raise ValueError(f"Specified output impedance not supported.\nMust be one of INF, MIN, MAX or between 1 and 10k ohms")
        return self.write(f"OUTP{self.channel}:LOAD {value}")
        
    @property
    def output(self):
        return 'ON' if int(self.query(f"OUTP{self.channel}?")) else 'OFF'
    
    @output.setter
    def output(self, key):
        if key not in ['ON', 'OFF']:
            raise ValueError(f'Key >>{key}<< invalid.\nMust be one of ON, OFF')
        return self.write(f"OUTP{self.channel} {key}")
        
    # disconnect procedures
    def disconnect(self):
        for c in range(1, config['NCHANNELS']+1):
            self[c].output = 'OFF'
        return super().disconnect()
    
    def screenshot(self):
        byte_data = self.bquery(f"HCOP:SDUM:DATA?")
        img = Image.open(io.BytesIO(byte_data))
        img.save('sshot.PNG')
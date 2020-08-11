from .SCPI.VISA_Instrument import VISA_Instrument
import logging

config = {
        'id' : 'HAMEG,HMP4040,026043549,HW50020001/SW2.50',
        'voltage' : {'max' : 32.05, 'min' : 0.0, 'step' : 0.001},
        'current' : {'max' : 10.01, 'min' : 0.0},
        'NCHANNELS' : 4
    }

class HMP4040(VISA_Instrument):
    
    # in case we need to extend the functionality of the init 
    def __init__(self, port=None, backend=''):
        # resource_params defined in config_dict
        super().__init__(port=port, backend=backend, read_termination = '\n')
        # TODO! Should internally check if device is HM4040
        logging.info("HMP4040: Successfully instanciated")
    
    # TODO! implement repr 
    def __repr__(self):
        ret = []
        ret.append("HMP4040 Power Supply")
        ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
        ret.append(super().__repr__())
        if self.connected:
            #for channel in range(1, config['NCHANNELS']+1):
            ret.append(f"Channel: {self.channel}")
            ret.append(f"Voltage: {self.voltage}")
            ret.append(f"Current: {self.current}")
        return '\n'.join([r for r in ret])
    
    def __getitem__(self, key):
        if key not in range(1, config['NCHANNELS']+1):
            raise ValueError(f"HMP4040 has {config['NCHANNELS']} channels")    
        self.channel = key
        return self


    @property
    def channel(self):
        """
        Queries the current device channel
        """
        return self.INST.NSEL()
    
    @channel.setter
    def channel(self, channel : int):
        """
        Selects a channel using a numerical value
        Number of channels physically defined by NUM_CHANNELS
        
        channel: channel number (between and including 1 - 4)
        
        """
        if channel not in range(1, config['NCHANNELS']+1):
            raise ValueError(f"HM4040: Specified channel >>{channel}<< not available")
        
        return self.INST.NSEL(channel)
        
        
    @property
    def voltage(self):
        """
        Get channel voltage
        """
        return self.VOLT()
        
    # setting voltages
    @voltage.setter
    def voltage(self, value : float):
        """
        Sets the voltage on a current channel to a value
        between 0 [MIN] and 32.05 [MAX]
        
        """
        if not config['voltage']['min'] < value < config['voltage']['max']:
            raise ValueError(f"Specified voltage outside device bounds: {value} [V]")
        if (float(value)//(float(config['voltage']['step'])) % 1):
            raise ValueError("Specified discretisation not supported")
        
        return self.VOLT(value)
        
    
    @property
    def current(self):
        """
        Get channel current
        """
        return self.CURR()
        
    # setting voltages
    @current.setter
    def current(self, value : float):
        """
        Sets the current on the current channel to a value
        between 0 [MIN] and 10.010 A [MAX]
        """
        if not config['current']['min'] < value < config['current']['max']:
            raise ValueError(f"Specified current outside device bounds: {value}")
        if (float(value)//(float(config['current']['step'])) % 1):
            raise ValueError("Specified discretisation not supported")
        
        return self.CURR(value)

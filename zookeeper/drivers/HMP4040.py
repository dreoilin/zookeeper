from .SCPI.VISA_Instrument import VISA_Instrument
import logging

config = {
        'id' : 'HAMEG,HMP4040,026043549,HW50020001/SW2.50',
        'voltage' : {'max' : 32.05, 'min' : 0.0},
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
        ret.append(f"HMP4040 Power Supply")
        ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
        ret.append(f"Port: {self.__port}")
        if self.connected:
            ret.append(f"Instrument connected")
            ret.append(f"Manufacturer ID: {self.id}")
            ret.append(f"Current channel: {self.channel}")
        return '\n'.join([r for r in ret])
    
    def _startup(self):
        self.CLS()
        self.RST()    
    
    def connect(self):
        super().connect()
        self._startup()

    # HMP4040 does not support parallel processing
    def _synchronise(self):
        # set operation complete
        self.OPC()
        # query for completion
        return (1 == int(self.OPC('?')))

    @property
    def channel(self):
        """
        Queries the current device channel
        """
        ret = int(self.INST.NSEL())
        if self._synchronise():
            return ret
        else:
            return None
    
    @channel.setter
    def channel(self, channel : int):
        """
        Selects a channel using a numerical value
        Number of channels physically defined by NUM_CHANNELS
        
        channel: channel number (between and including 1 - 4)
        
        """
        if channel not in range(1, config['NCHANNELS']+1):
            logging.warning("HM4040: Specified channel not available")
            return None
        
        ret =  self.INST.NSEL(channel)
        if self._synchronise():
            return ret
        else:
            return None
        
    @property
    def voltage(self):
        """
        Get channel voltage
        """
        ret = float(self.VOLT())
        
        if self._synchronise():
            return ret
        else:
            return None
        
    # setting voltages
    @voltage.setter
    def voltage(self, value : float):
        """
        Sets the voltage on a current channel to a value
        between 0 [MIN] and 32.05 [MAX]
        
        """
        if not config['voltage']['min'] < value < config['voltage']['max']:
            logging.warning(f"Specified voltage outside device bounds: {value}")
            return
        
        ret = self.VOLT(value)
        
        if self._synchronise():
            return ret
        else:
            return
    
    @property
    def current(self):
        """
        Get channel current
        """
        ret = float(self.CURR())
        
        if self._synchronise():
            return ret
        else:
            return None
        
    # setting voltages
    @current.setter
    def current(self, value : float):
        """
        Sets the current on the current channel to a value
        between 0 [MIN] and 10.010 A [MAX]
        """
        if not config['current']['min'] < value < config['current']['max']:
            logging.warning(f"Specified current outside device bounds: {value}")
            return
        
        ret = self.CURR(value)
        
        if self._synchronise():
            return ret
        else:
            return None

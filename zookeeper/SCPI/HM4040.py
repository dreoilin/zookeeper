from .SCPI_Instrument import Instrument
import logging

ID = 'HAMEG,HMP4040,026043549,HW50020001/SW2.50\n'
NUM_CHANNELS = 4
VOLTAGE = {'MIN': 0.0, 'MAX' : 32.05}
config = {
    
    }

class HM4040(Instrument):
    
    # in case we need to extend the functionality of the init 
    def __init__(self, port=None, backend=''):
        # resource_params defined in config_dict
        super().__init__(port=port, backend=backend, resource_params=config)
        # self._startup()
        # TODO! Should internally check if device is HM4040
        logging.info("HM4040: Successfully instanciated")
    
    # TODO! implement repr 
    def __repr__(self):
        pass
    
    def _startup(self):
        self.CLS()
        self.RST()    
            
    @property
    def channel(self):
        """
        Queries the current device channel
        """
        return self.INST.NSEL()
    
    @channel.setter
    def channel(self, channel : int = None):
        """
        Selects a channel using a numerical value
        Number of channels physically defined by NUM_CHANNELS
        
        channel: channel number (between and including 1 - 4)
        
        """
        if channel not in range(1, NUM_CHANNELS+1):
            logging.warning("HM4040: Specified channel not available")
            return
        return self.INST.NSEL(channel)
    
    @property
    def voltage(self, channel : int = None):
        pass
    
    # setting voltages
    @voltage.setter
    def voltage(self, channel : int = None):
        """
        Sets the voltage on a specified channel to a value
        between 0 [MIN] and 32.05 [MAX]
        
        channel :   optional channel value. if unspecified, defaults to
                    current channel
        """
        if channel not in range(1, NUM_CHANNELS+1):
            logging.warning("HM4040: Specified channel not available")
            return
        
        # TODO! Implement voltage setter
        pass
from .SCPI.VISA_Instrument import VISA_Instrument
import logging

class KSMSO(VISA_Instrument):
    def __init__(self, port=None, backend=''):
        super().__init__(port=port, backend='', read_termination='\n')
        logging.info("KSMSO: Successfully instanciated")
        self.channel = 1
        
    @property
    def channel(self):
        return self.__channel
    
    @channel.setter
    def channel(self, key):
        self.__channel = key
        
class ChannelManager(object):
    channel_types = ('ANA', 'DIG')
    def __init__(self, **kwargs):
        # private member dict to hold channels
        self.__nchannels = {k:v for k,v in kwargs if k in channel_types}
        self.__channel = {k:1 for k in channel_types}
    
    def __repr__(self):
        ret = [f"{key}: {self.__nchannels[key]} channels" for key in channel_types]
        ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
        ret.extend([f"{key}: {self.__channel[key]} selected" for key in channel_types])
        return ret
    
    def __getitem__(self, key):
        if key in channel_types:
            return self.__channel[key]
        else:
            raise KeyError('Device does not support this type of channel\nMust be one of ANA, DIG')
        
    def __setitem__(self, key, value):
        if key in channel_types and 0 < value <=self.nchannels[key]:
            self.__channel[key] = value
        else:
            raise KeyError('Device does not support this type of channel\nMust be one of ANA, DIG')
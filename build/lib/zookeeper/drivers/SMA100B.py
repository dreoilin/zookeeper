from .SCPI.VISA_Instrument import VISA_Instrument
from PIL import Image
import io
import logging

config = {}

class SMA100B(VISA_Instrument):
    def __init__(self, port=None, backend=''):
        super().__init__(port=port, backend=backend, read_termination = '\n', timeout=None)
        self.__channel = 1
        logging.info("SMA100B: Successfully instanciated")
        
    @property
    def channel(self):
        return self.__channel
    
    @channel.setter
    def channel(self, key):
        self.__channel = key
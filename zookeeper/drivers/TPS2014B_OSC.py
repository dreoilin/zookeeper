from .SCPI.VISA_Instrument import VISA_Instrument
import logging
from PIL import Image
from datetime import datetime
import io
import re

config = {
    'NCHANNELS' : 4
    }

class TPS2014B_OSC(VISA_Instrument):
    def __init__(self, port = None):
        super().__init__(port=port, write_termination='\n', \
                read_termination='\n', timeout=10000)
        logging.info("TSP2014B_OSC: Successfully instanciated")
        self.channel = 1
        
    def __repr__(self):
        ret = []
        ret.append("KS33522B Signal Generator")
        ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
        ret.append(super().__repr__())
        if self.connected:
            ret.appedn('Connected')

        return '\n'.join([r for r in ret])
        
    def __getitem__(self, key):
        if key not in range(1, config['NCHANNELS']+1):
            raise ValueError(f"TSP2014B_OSC: supports {config['NCHANNELS']} channels")
        
        self.channel = key
        return self
 
    def connect(self):
        super().connect()
        logging.info("KS33522B: performing startup procedure")
        self.__startup()
    
   
    @property
    def channel(self):
        return self.__channel
    
    @channel.setter
    def channel(self, channel : int):
        if not 1 <= channel <= config['NCHANNELS']:
            raise ValueError(f"Specified channel does not exist: {channel}")
            
        self.__channel = channel
               
    # disconnect procedures
    def disconnect(self):
        for c in range(1, config['NCHANNELS']+1):
            self[c].output = 'OFF'
        return super().disconnect()
    
    def screenshot(self, filename=None, format='BMP'):
        if filename is None:
            filename = f'sshot_{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")}'
        self.write(f'HARDC:FORMAT {format}')
        byte_data = self.bquery(f"HARDC STAR")
        img = Image.open(io.BytesIO(byte_data))
        img.save(f'{filename}.{format}')

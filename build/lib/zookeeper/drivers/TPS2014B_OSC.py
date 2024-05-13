from .SCPI.VISA_Instrument import VISA_Instrument
import logging
from PIL import Image
from datetime import datetime
import io
import re
import numpy as np

headers = {  'BYT_NR' : int,
            'BIT_NR' : int,
            'ENCDG' : str,
            'BN_FMT' : str,
            'BYT_OR' : str,
            'NR_PT' : int,
            'WFID' : str, 
            'PT_FMT' : str,
            'XINCR' : float, 
            'PT_OFF' : float, 
            'XZERO' : float,
            'XUNIT' : str,
            'YMULT' : float,
            'YZERO' : float,
            'YOFF' : float,
            'YUNIT' : str }

config = {
    'NCHANNELS' : 4
    }

class TPS2014B_OSC(VISA_Instrument):
    def __init__(self, port = None):
        super().__init__(port=port, baud_rate=19200, write_termination='\n', read_termination='\n', timeout=None)
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
        #for c in range(1, config['NCHANNELS']+1):
        #    self[c].output = 'OFF'
        return super().disconnect()
    
    def _get_and_parse_waveform_header(self):

        header = self.query('WFMP?')
        vals = header.split(';')
        ret = {}
        for i, key in enumerate(headers.keys()):
            ret[key] = headers[key](vals[i])
        
        wfid = ret['WFID'].split(', ')
        

        return ret
    
    def _get_waveform(self):
        return np.array(self.query_ascii_values('CURV?'))

    def waveform(self):
        hdata = self._get_and_parse_waveform_header()
        wvdata = self._get_waveform()
        # build wave here and return dict with numpy arrays and header values
        N = len(wvdata)
        x = np.zeros(wvdata.shape)
        y = np.zeros(wvdata.shape)
        x = np.arange(hdata['XZERO'], N*hdata['XINCR'], hdata['XINCR'])
        y = wvdata + np.ones(wvdata.shape)*hdata['YZERO']
        return (x, y)

    def screenshot(self, filename=None, format='BMP'):
        if filename is None:
            filename = f'sshot_{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")}'
        self.write(f'HARDC:FORMAT {format}')
        byte_data = self.bquery(f"HARDC STAR")
        img = Image.open(io.BytesIO(byte_data))
        img.save(f'{filename}.{format}')

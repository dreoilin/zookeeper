import logging
import configparser
from os import path
import collections
from .drivers.KS33522B import KS33522B
from .drivers.HMP4040 import HMP4040
from .drivers.SMA100B import SMA100B
from .drivers.AGI33210A_WG import AGI33210A_WG
from .drivers.AGI34410A_MM import AGI34410A_MM
from .drivers.AGIE3633A_PS import AGIE3633A_PS
from .drivers.DSP7265_LIA import DSP7265_LIA
from .drivers.TPS2014B_OSC import TPS2014B_OSC
from .drivers.KEPCO_BPS import KEPCO_BPS
from .drivers.SRS_LIA import SRS_LIA
from .drivers.SCPI.VISA_Instrument import VISA_Instrument

# safer than using globals()
supported = {
    'KS33522B' : KS33522B,
    'HMP4040'  : HMP4040,
    'SMA100B'  : SMA100B,
    'AGI33210A_WG' : AGI33210A_WG,
    'AGIE3633A_PS' : AGIE3633A_PS,
    'DSP7265_LIA' : DSP7265_LIA,
    'KEPCO_BPS' : KEPCO_BPS,
    'TPS2014B_OSC' : TPS2014B_OSC,
    'SRS_LIA' : SRS_LIA
    }

class Workbench(collections.Mapping):
    def __init__(self, configfile='devices.ini'):
        self.__configpath = configfile
        self.__config = configparser.ConfigParser()
        self.__instruments = {}
        self.__setup()
    
    def __repr__(self):
        return '\n\n'.join(['\n'.join([key ,self.__instruments[key].__repr__()]) for key in self.__instruments.keys()])
    
    def __setup(self):
        
        self.__config.read(self.__configpath)
        for devname in self.__config.sections():
            model = self.__config[devname]['device']
            port = self.__config[devname]['port']
            try:
                inst = supported[model](port=port)
            except KeyError:
                logging.error("Device is not currently supported.")
            try:
                self.__instruments[devname] = inst
            except KeyError:
                logging.warning(f"Device of same name `{devname}' already exists. Change to another.")
    
    def __getitem__(self, key):
        return self.__instruments[key]
    
    def __len__(self):
        return len(self.__instruments)
    
    def __iter__(self):
        return iter(self.__instruments)
    
    def connect(self):
        for device in self.__instruments.values():
            device.connect()
    
    def disconnect(self):
        for device in self.__instruments.values():
            device.disconnect()

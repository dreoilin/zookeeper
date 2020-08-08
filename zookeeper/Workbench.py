import logging
import configparser
from os import path
import collections
from .drivers.KS33522B import KS33522B
from .drivers.HMP4040 import HMP4040
from .drivers.SCPI.VISA_Instrument import VISA_Instrument

# safer than using globals()
supported = {
    'KS33522B' : KS33522B,
    'HMP4040'  : HMP4040
    }

class Workbench(collections.Mapping):
    def __init__(self, configfile='devices.ini'):
        basepath = path.dirname(__file__)
        self.__configpath = path.abspath(path.join(basepath, '..', configfile))
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
                logging.warning(f"Device of same name `{key}' already exists. Change to another.")
    
    def __getitem__(self, key):
        return self.__instruments[key]
    
    def __len__(self):
        return len(self.__instruments)
    
    def __iter__(self):
        return iter(self.__instruments)
    
    def connect(self):
        [device.connect() for device in self.__instruments.values()]

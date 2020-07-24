import vxi11
import logging
from .SCPI_Instrument import Instrument

class vxi11_Instrument(Instrument):
    def __init__(self, host=None):
        # need nicer method of setting timeout
        self.__host = host
        self.__instrument = None
        
    def __del__(self):
        if self.conected:
            self.disconnect()
            
        del self.__instrument
        
    def connect(self):
        if self.__instrument is None:
            self.__instrument = vxi11.Instrument(self.__host)

        else:
            self.__instrument.open()
    
    @property
    def connected(self):
        # not my proudest bit of code
        if self.__instrument is not None:
            return True
        else:
            return False
    
    def disconnect(self):
        if self.__instrument is not None:
            self.__instrument.close()
    
    @property
    def instrument(self):
        return self.__instrument
    
    @property
    def host(self):
        return self.__host
    
    @host.setter
    def host(self, host):
        """
        Disconnect and update port

        """
        if self.__instrument is not None:
            self.disconnect()
        
        self.__host = host
    
    @property
    def status(self):
        return self.__instrument.read_stb()
        
    def write(self, msg):
        """
        Performs a SCPI write operation on the resource
        msg : write value
        """
        if self.__instrument is None:
            raise Exception( 'Can not write, instrument not connected.' )
            return
            
        return self.__instrument.write(msg)
            
            
    def read(self):
        """
        Performs a SCPI read operation on the resource
        """
        if self.__instrument is None:
            raise Exception( 'Can not read, instrument not connected' )
            return
            
        return self.__instrument.read()
    
    
    def query(self, msg):
        """
        Performs a SCPI read/write query operation on the resource
        msg : write value
        ret : read value from resource
        """
        if self.__instrument is None:
            raise Exception( 'Can not query, instrument not connected' )
        
        return self.__instrument.ask(msg)
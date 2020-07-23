import pyvisa as visa
import logging

ASCII = list(range(0, 255))
LOC = list(range(0, 9))

COMMON = {
'CLS' : [None], # CLear Status (W) : reset STB, ESR
'ESE' : [*ASCII, '?'], # Event Status Enable (0-255, ?) : arg->sets register, ?->queries register
'ESR' : ['?'], # Event Status Read (?) : returns ES register and resets to 0
'IDN' : ['?'], # IDenTification (?) : returns device ID
'OPC' : [None, '?'], # OPeration Complete (W, ?) : W sets bit 0 ? writes 1 to output on completion
'RST' : [None], # ReSeT (W) : sets to defined status
'SRE' : [*ASCII], # Service Request Enable (0-255) : sets service request register
'STB' : ['?'], # STatus Byte query (?) : returns status byte (decimal)
'TST' : ['?'], # self TeST (?) : triggers selftests->0 no error
'WAI' : [None], # WAIt to continue (W) : prevent servicing subsequent commands until all executed
'SAV' : [*LOC], # SAV {0|1|2|3 ...} (0-9) : saves data to location
'RCL' : [*LOC] # RCL {0|1|2 ...} (0-9) : recalls current instrument state
}

class Command(object):
    
    def __init__(self, instrument, attr):
        self.__instrument = instrument
        self.attr = attr.upper()
        
    def __getattr__(self, attr):
        """
        Recursively construct the query or write directive
        by joining parts of the request with :
        """
        return Command(
            self.__instrument,
            ':'.join((self.attr, attr.upper()))
            )
    
    def __call__(self, value=None):
        """
        Properties are either queries or write requests.
        
        Terminate hierarchial queries with ?
        and write directive with their corresponding value
        """
        if value is None:
            return self.__instrument.query(self.attr + '?')
        else:
            if not isinstance(value, str):
                value = str(value)
                
        return self.__instrument.write(self.attr + ' ' + value)

class Instrument():
    """
    A SCPI (skippy) instrument
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    
    def __init__(self):
        pass
 
    def __getattr__(self, attr):
        """
        Dunder method to allow for pythonic commands
        """
        # case 1 - common commands
        if attr.upper() in COMMON.keys():
            def common(*args):
                return self.COMMON(attr.upper(), *args)
            
            return common
        # finally, just deal with it as device specific
        return Command(self, attr)  
   
    def COMMON(self, command, key=None):
        """
        Deals with the common commands
        """
        if key not in COMMON[command]:
            raise ValueError(f'Argument {key} not supported in common command')
        else:
            if key is None:
                logging.debug(f"No key. CMD:\n *{command}")
                return self.write(f"*{command}")
            elif key == '?':
                logging.debug(f"Query key. CMD: \n *{command}?")
                return self.query(f"*{command}?")
            elif str(key).isnumeric():
                logging.debug(f"Numeric key. CMD: \n *{command} {key}")
                return self.write(f"*{command} {key}") 
   
    @property
    def id(self):
        """
        Queries the lab instrument for the manufacturer ID
        """
        return self.query('*IDN?')
    
   
    # Read, Write, and Read/Write (query) commands
            
    def write(self, msg):
        pass   
            
    def read(self):
       pass

    def query(self, msg):
       pass            
    

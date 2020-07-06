from .SCPI_Instrument import Instrument
import logging

config = {
    'id' : 'HAMEG,HMP4040,026043549,HW50020001/SW2.50\n'
    
    }

class HM4040(Instrument):
    
    # in case we need to extend the functionality of the init 
    def __init__(self, port=None, backend=''):
        # resource_params defined in config_dict
        super().__init__(port=port, backend=backend, resource_params=config)
        
    def connect(self):
        # need exception handling here
        super().connect()
        if self.connected():
            self.startup()
        
    def startup(self):
        self.CLS()
        self.RST()    
    
    def select_channel(channel=None):
        if channel is None:
            logging.warning("HM4040: No channel selected")
            
        
    #def change_channel(self, num=None):
        
    #    self.channel.select(num)
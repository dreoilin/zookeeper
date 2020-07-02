from .SCPI_Instrument import Instrument

class HM4040(Instrument):
    
    
    def change_channel(self, num=None):
        
        self.channel.select(num)
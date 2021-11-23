from .SCPI.VISA_Instrument import VISA_Instrument
import logging
from time import sleep

config = {
        'voltage' : {'max' : 32.05, 'min' : 0.0, 'places' : 3},
        'current' : {'max' : 10.01, 'min' : 0.0, 'places' : 3}
    }

class AGIE3633A_PS(VISA_Instrument): 
    def __init__(self, port=None, backend=''):
        super().__init__(port=port, backend=backend, read_termination = '\n', timeout=None)
        logging.info("AGIE3633A_PS: Successfully instanciated")
     
    def __repr__(self):
        ret = []
        ret.append("AGIE3633A Power Supply")
        ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
        ret.append(super().__repr__())
        if self.connected:
            ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
            ret.append(f"Voltage: {self.voltage} [V]\tCurrent: {self.current} [A]")
            ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
            ret.append("Measurements across Sense Resistor") 
            ret.append("~~~~~~~~~~~~~~~~~~~~~~~~")
            ret.append(f"Voltage: {self.measure('VOLT')} [V]\tCurrent: {self.measure('CURR')} [A]")
            ret.append(f"Output is: {self.output}")
        
        return '\n'.join([r for r in ret])
    
    def connect(self):
        """
        Executes startup routines
        Channel voltages and currents are zeroed.
        Channel outputs are turned off
        """
        super().connect()
        self.apply(voltage = 0.0, current = 0.0)
        self.output = 'OFF'
            
    def disconnect(self):
        """
        Runs device shutdown routines.
        All outputs are turned off
        """
        self.output = 'OFF'
        
        return super().disconnect()
        
    @property
    def voltage(self):
        """
        Get channel voltage
        """
        return float(self.VOLT())
        
    # setting voltages
    @voltage.setter
    def voltage(self, value : float):
        """
        Sets the voltage on a current channel to a value
        between 0 [MIN] and 32.05 [MAX]
        
        Parameters
        ----------
        voltage : float
        """
        if not config['voltage']['min'] <= value <= config['voltage']['max']:
            raise ValueError(f"Specified voltage : {value} [V] outside device bounds\n Min: config['voltage']['min'] Max: config['voltage']['max']")
        
        return self.VOLT(round(value, config['voltage']['places']))
        
    
    @property
    def current(self):
        """
        Get channel current
        """
        return float(self.CURR())
        
    # setting voltages
    @current.setter
    def current(self, value : float):
        """
        Sets the current on the current channel to a value
        between 0 [MIN] and 10.010 A [MAX]
        
        Parameters
        ----------
        current : float
    
        """
        
        return self.CURR(round(value, config['current']['places']))
    
    def __configuration(self):
        """
        Private method to view voltage/current information from
        selected channel all at once
        """
        return self.APPLY()
    
    def apply(self, voltage : float = 0.0, current : float = 0.0):
        """
        Method to batch apply a voltage and current to the selected channel
        
        Parameters
        ----------
        voltage : float
        current : float
        """
        
        return self.APPLY(f"{voltage},{current}")
    
    @property
    def output(self):
        """
        Returns channel output status
        
        Returns:
        --------
           str:
            'ON' or 'OFF'
        """
        return 'ON' if int(self.OUTP()) else 'OFF'
    
    @output.setter
    def output(self, key):
        """
        Controls the channel output

        Parameters
        ----------
        key : int/str
            Turn on output -> 'ON' or 1
            Turn off output -> 'OFF' or 0
        
        """
        if key in ['ON', 1]:
            return self.OUTP('ON')
        elif key in ['OFF', 0]:
            return self.OUTP('OFF')
        else:
            raise ValueError("Key invalid. Must be one of:\n ON, OFF, 1, 0")
        
    def measure(self, quantity='VOLT'):
        if quantity not in ['VOLT', 'CURR']:
            raise ValueError('Cannto measure specified quantity.')
        return self.query('MEAS:{quantity}?')

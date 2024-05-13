from .SCPI.VISA_Instrument import VISA_Instrument
import logging

MEASUREMENTS = ['CPD',
                'CPQ',
                'CPG',
                'CPRP',
                'CSD',
                'CSQ',
                'CSRS',
                'LPD',
                'LPQ',
                'LPG',
                'LPRP',
                'LPRD',
                'LSD',
                'LSQ',
                'LSRS',
                'LSRD',
                'RX',
                'ZTD',
                'ZTR']

class E4980_LCR(VISA_Instrument):
    def __init__(self, port = None):
        super().__init__(port=port, read_termination='\n')
        logging.info("E4980 LCR: Successfully instanciated")
        
    def connect(self):
        super().connect()
        logging.info("E4980A LCR Meter: performing startup procedure")
   
    # automatic level control
    @property
    def ALC(self):
        return self.query(f":AMPL:ALC?")
    
    @ALC.setter
    def ALC(self, key='ON'):
        return self.write(f":AMPL:ALC {key}")
    
    # automatic level control
    @property
    def aperture(self):
        return self.query(f":APER?")
    
    @aperture.setter
    def aperture(self, key='LONG'):
        if key not in ['SHORT', 'MEDIUM', 'LONG']:
            raise ValueError("Key invalid. Must be one of SHORT, MEDIUM, LONG")
        return self.write(f":AMPL:ALC {key}")
    
    @property
    def impedance(self):
        return self.query(':FUNC:IMP?')

    @impedance.setter
    def impedance(self, key='CPD'):
        if key not in MEASUREMENTS:
            raise ValueError('Invalid measurement type')
        return self.write(f':FUNC:IMP {key}')
    
    @property
    def frequency(self):
        return self.query(':FREQ?')

    @frequency.setter
    def frequency(self, key=1e3):
        return self.write(f':FREQ {key}')

    @property
    def autorange(self):
        return self.query(':FUNC:IMP:RANG:AUTO?')

    @autorange.setter
    def autorange(self, key='ON'):
        return self.write(f':FUNC:IMP:RANG:AUTO {key}')

    @property
    def Ibias(self):
        return float(self.query(':BIAS:CURR?'))
    
    @Ibias.setter
    def Ibias(self, value=0):
        return self.write(f':BIAS:CURR {value}')
    
    @property
    def bias(self):
        return self.query(':BIAS:STAT?')

    @bias.setter
    def bias(self, key=1):
        return self.write(f':BIAS:STAT {key}')

    # disconnect procedures
    def disconnect(self):
        self.output = 'OFF'
        return super().disconnect()
    
    def fetch(self):
        return str(self.query(f':FETCH?'))

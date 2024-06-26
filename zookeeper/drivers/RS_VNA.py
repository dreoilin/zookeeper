
from .SCPI.VISA_Instrument import VISA_Instrument
import logging
import numpy as np
from time import sleep
import math

config = {
    'NCHANNELS' : 4
}

class RS_VNA(VISA_Instrument):
    def __init__(self, port = None):
        # debug read and write termination
        super().__init__(port=port, timeout=10000)
        logging.info("R&S VNA: Successfully instanciated")
        self.channel = 1

    def connect(self):
        super().connect()
        logging.info("R&S VNA: connected")

    def __getitem__(self, key):
        if key not in range(1, config['NCHANNELS']+1):
            raise ValueError(f"VNA has {config['NCHANNELS']} channels")    
        self.channel = key
        return self

    def __complex2dB__(self, data):
        """Calculate Re/Im --> dB"""
        outArry = []
        if len(data) % 2 == 0:
            for i in range(len(data)//2):
                magnitude = math.sqrt(data[2*i] ** 2 + data[2*i+1] ** 2)
                outArry.append(20 * math.log10(magnitude))
        else:
            logging.info('Need even elements')
        return outArry

    def __complex2phase__(self, data):
        """Calculate Re/Im --> phase"""
        outArry = []
        if len(data) % 2 == 0:
            for i in range(len(data)//2):
                phase = math.degrees(math.atan(data[2*i+1]/data[2*i]))
                outArry.append(phase)
        else:
            logging.info('Need even elements')
        return outArry

    def __complex2dBm__(self, data):
        """Calculate Re/Im --> dBm"""
        outArry = []
        if len(data) % 2 == 0:
            for i in range(len(data)//2):
                magnitude = math.sqrt((data[2*i] ** 2 + data[2*i+1] ** 2)/50)
                outArry.append(20 * math.log10(magnitude) + 30)
        else:
            logging.info('Need even elements')
        return outArry

    #####################################################################
    ### VNA GET Functions Alphabetical
    #####################################################################
    def Get_Pwrcal_Rx_State(self):
        rdStr = self.query(f':SENS:CORR:STAT?')
        return rdStr

    def Get_Pwrcal_State(self):
        rdStr = self.query(f':SOUR:POW:CORR:STAT?')
        return rdStr

    def Get_Trace_Data(self):
        """Retrive Formatted Data: Data Only"""
        self.write('FORM ASCII')
        rdStr = self.queryFloatArry(f':CALC{self.dChan}:DATA:DALL? FDAT')
        return rdStr

    def Get_Trace_Data_All(self):
        """Retrive Formatted Data: Memory & Data"""
        self.write('FORM ASCII')
        rdStr = self.queryFloatArry(f':CALC{self.dChan}:DATA:ALL? FDAT')
        return rdStr

    # def Get_Trace_Data_CAll(self):
    #     """Retrive Formatted Data: nxn matrix S-Param"""
    #     self.write('FORM ASCII')
    #     rdStr = self.queryFloatArry(f':CALC{self.dChan}:DATA:CALL? FDAT')
    #     return rdStr

    def Get_Trace_Names(self):
        rdStr = self.query(f':CALC{self.dChan}:PAR:CAT?')
        return rdStr

    #####################################################################
    ### VNA SAVE Functions Alphabetical
    #####################################################################
    def Save_Cal(self, sFName):
        """ Save calibration to cal manager """
        if not sFName.lower().endswith(f'.cal'): 
            sFName += ".cal"
        self.write(f':MMEM:STOR:CORR {self.dChan},"{sFName}"')

    def Save_Screen(self,sFName):
        """ Save Sceen to BMP """
        self.write('HCOP:DEV:LANG BMP')
        self.write(f'MMEM:NAME "{sFName}.BMP"')
        self.write('HCOP:DEST "MMEM"; :HCOP')

    def Save_State(self, sFName):
        """ Save State """
        self.write(f'MMEM:STOR:STAT 1,"{sFName}"')

    def Save_Trace_CSV(self, sFName):
        """Save Data in dB Phase CSV format"""
        # self.write(f'MMEM:STOR:TRAC:CHAN "{sTrace}","{sFName}.csv",FORM, LOGP, POIN, COMM')
        # self.write(f'MMEM:STOR:TRAC:CHAN "{sTrace}","{sFName}.csv",UNF, COMP, POIN, COMM')
        self.write(f"MMEM:STOR:TRAC:CHAN ALL,'{sFName}.csv', UNF, LOGP, POIN, COMM")

    def Save_Trace_SxP(self, sFName):                                   # MMM
        """Save SxP data.  Ch must contain All (x^x) S-Parameter traces"""
        self.write(f"MMEM:STOR:TRAC:CHAN 1,'C:\\Rohde&Schwarz\\Nwa\\{sFName}.s2p'")
        #self.write(f':MMEM:STOR:TRAC:PORT %d,'%s.s2p',COMP,1,2"%(dChan,sFName))

    #####################################################################
    ### VNA SET Functions Alphabetical
    #####################################################################
    # def Set_Cal_Group(self,sName,dChan=1):                            # MMM
    #     #sName should end in '.cal'
    #     if not sName.lower().endswith(f'.cal'):
    #         sName += ".cal"
    #     self.write(f':MMEM:LOAD:CORR:RES %d,%s"%(dChan,sName))        # Resolve Cal Group
    #     self.write(f':MMEM:LOAD:CORR %s"%(sName))                     # Load cal group.

    def Set_FreqStart(self,fFreq):
        self.write(f':SENS{self.dChan}:FREQ:STAR {fFreq}')

    def Set_FreqStop(self,fFreq):
        self.write(f':SENS{self.dChan}:FREQ:STOP {fFreq}')              # RF Freq

    def Set_IFBW(self,fFreq):
        self.write(f'SENS{self.dChan}:BAND {fFreq}')

    def Set_InitImm(self):
        self.query(f'INIT:IMM;*OPC?')

    def Set_Mkr_Coupled(self, state):
        if state in (1,'1', 'ON'):
            self.write(f'CALC{self.dChan}:MARK:COUP ON')
        elif state in (0,'0', 'OFF'):
            self.write(f'CALC{self.dChan}:MARK:COUP OFF')

    def Set_Mkr_Frq(self, frq, mkr=1):
        # self.write(f'CALC{self.dChan}:MARK{mkr} ON')
        # self.write(f'CALC{self.dChan}:MARK{mkr} {frq}')
        self.write(f'CALC:MARK{mkr}:STAT ON')
        self.write(f'CALC:MARK{mkr}:X {frq:.0f}')

    def Set_PowerStart(self, fPwr):
        self.write(f':SOUR{self.dChan}:POW:STAR {fPwr} dBm')

    def Set_PowerStop(self, fPwr):
        self.write(f':SOUR{self.dChan}:POW:STOP {fPwr} dBm')

    def Set_Pwrcal_Init(self):
        self.write(f':SOUR:POW:CORR:COLL:FLAT ON')      # Flatness Cal
        self.write(f':SOUR:POW:CORR:COLL:RREC ON')      # Ref Rx Cal
        self.write(f':SOUR:POW:CORR:COLL:VER ON')       # Verification Sweep
        self.write(f':SOUR:POW:CORR:COLL:METH PMON')    # PMON | RFAF | RRON

    def Set_Pwrcal_NumReading(self, iNum):
        self.write(f':SOUR{self.dChan}:POW:CORR:NRE {iNum}')

    def Set_Pwrcal_Measure(self, iPort):
        self.write(f':SOUR{self.dChan}:POW:CORR:ACQ PORT,{iPort}')

    def Set_Pwrcal_Rx(self, Source, Port):
        # CORR:POW:ACQ <What to Cal> <Port>,<SourceTYpe>,<Port#>,<AWAV/NOM>
        self.write(f':CORR:POW:ACQ BWAV,{Port},PORT,{Source},AWAV')
        self.query('CORR:POW:AWAV?')

    def Set_Pwrcal_Tolerance(self,fTol):
        self.write(f':SOUR:POW:CORR:COLL:AVER:NTOL {fTol}')

    def Set_SweepCont(self,sState):
        if sState in (1, 'ON'):
            self.write(f'INIT:CONT ON')                                 # Continuous Sweep
        elif sState in (0, 'OFF'):
            self.write(f'INIT:CONT OFF')                                # Single Sweep

    def Set_SweepPoints(self,dPoints):
        self.write(f':SENS{self.dChan}:SWE:POIN {dPoints}')             # RF Freq

    def Set_SweepTime(self,fSwpTime):
        """Seconds. 0=Auto"""
        if fSwpTime == 0:
            self.write(f':SENS{self.dChan}:SWE:TIME:AUTO ON')           # Auto
        else:
            self.write(f':SENS{self.dChan}:SWE:TIME {fSwpTime}')        # Sweep/Capture Time

    def Set_Trace_Avg(self,sState):
        if sState in (1, 'ON'):
            self.write(f':SENS{self.dChan}:AVER:STAT ON')
        if sState in (1, 'ON'):
            self.write(f':SENS{self.dChan}:AVER:STAT OFF')

    def Set_Trace_AvgCount(self,iAvg):
        self.write(f':SENS{self.dChan}:AVER:COUN {iAvg}')

    def Set_Trace_DelAll(self):
        self.write(f'CALC:PAR:DEL:ALL')

    def Set_Trace_MeasAdd(self,sMeas):
        # S11/S21/S12/S22 ..... Sxxyy
        # Y11/Y21/Y12/Y22 ..... Yxxyy
        # A1D2/A1D4/A2D1  ..... A<port>G<port>
        # B1D2/B1D4/B2D1  ..... B<port>G<port>
        # IP3UI/IP3UO      ..... IP<order:3|5|7|9><side:U|L><DUT:I|O>
        self.write(f'CALC{self.dChan}:PAR:SDEF "{sMeas}","{sMeas}"')    # <TrcName>,<Measurement>
        self.write(f'DISP:WIND1:TRAC:EFE "{sMeas}"')                    # Displays Trace

    def Set_Trace_MeasAdd_AWave(self,APort,GenPort):
        #Default: SAM; RMS; PEAK; AVG
        self.Set_Trace_MeasAdd(f'A{APort}D{GenPort}RMS')

    def Set_Trace_MeasAdd_BWave(self,BPort,GenPort):
        self.Set_Trace_MeasAdd(f'B{BPort}D{GenPort}RMS')

    # def Set_Trace_MeasAdd_IMD3(self,dChan=1):                         # mmm
    #     self.write(f':SENS{dChan}:FREQ:IMOD:ORD3 ON"%(dChan))
    #     self.Set_Trace_MeasAdd(f'IP3UI')
    #     self.Set_Trace_MeasAdd(f'IP3LI')

    def Set_Trace_MeasAdd_SParam(self,Port1,Port2):
        """Port1,Port2"""
        self.Set_Trace_MeasAdd(f'S{Port1}{Port2}')

    def Set_Trace_MeasAdd_PwrMtr(self,GenPort):
        self.Set_Trace_MeasAdd(f'Pmtr{1}D{GenPort}')

    def Set_Trace_MeasDel(self,sTrcName):
        self.write(f'CALC{self.dChan}:PAR:DEL "{sTrcName}"')

    def Set_Trace_Select(self,sTrcName):
        self.write(f'CALC{self.dChan}:PAR:SEL "{sTrcName}"')
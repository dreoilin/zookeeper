# from .SCPI.VISA_Instrument import VISA_Instrument
import logging
import serial
import numpy as np


class AMAXDAQ1():
    def __init__(self, port = None, fsample = 115200):
        # serial port e.g '/dev/ttyUSB0'
        self.comport = port 
        self.fsample = fsample
        logging.info("AMAXDAQ1: Successfully instanciated")

    def disconnect(self):
        self.handleComport.close()
        logging.info("AMAXDAQ1: Successfully instanciated")

    def sendCommand(self, cmd):
        """
        Write command to serial port
        
        msg : str
        """
        try:
            handleComport = serial.Serial(self.comport, self.fsample)
            handleComport.reset_output_buffer()
            handleComport.write(bytearray(str(cmd),'utf8'))
            handleComport.close()
        except:
            print("Error send command")

    def getModuleId(self):
        moduleId = 0 # Default error value
        try:# Timeouts, because this function is a "gate keeper" to the program
            handleComport = serial.Serial(self.comport, self.fsample, timeout = 0.5, write_timeout = 0.5)
            handleComport.reset_output_buffer()
            handleComport.reset_input_buffer()
            handleComport.write(bytearray("?", 'utf8'))        
            moduleId = int(handleComport.read())
            handleComport.close()
        except:
            print("Error determine module ID")
        return moduleId
        
        
    def dataCollect(self, samples, target):    
        # Function variables
        adcSamples = 16384
        adcByteList = 0
        adcSignalVolt = []    
        adcSignalFloatNormalized = []
        adcSignedInteger = []
        # Connect to comport, clean buffer and get maximum sampling frequencie of the module
        handleComport = serial.Serial(self.comport, self.fsample)
        handleComport.reset_output_buffer()
        handleComport.write(bytearray("t",'utf8')) # Trigger the adc   
        # Collect the data
        for i in range(1, samples, 16):
            try:
                handleComport.reset_input_buffer()
                handleComport.write(bytearray("*",'utf8')) # Read 16384 adc values 
                if target == 1:
                    adcByteList = handleComport.read(5*adcSamples)
                    self.dataConvertTEI0015(adcByteList, adcSamples, adcSignalVolt, adcSignalFloatNormalized, adcSignedInteger)
                else:
                    adcByteList = handleComport.read(4*adcSamples)
                    self.dataConvertTEI0016(adcByteList, adcSamples, adcSignalVolt, adcSignalFloatNormalized, adcSignedInteger)
                adcByteList = 0           
            except:
                print("ADC data not aquired, stored or processed")
        handleComport.close()
        
        return [adcSignalVolt, adcSignalFloatNormalized, adcSignedInteger]
        
        
    # Separate binary data into single values and convert them to a  voltage list and a normalized list

    # ADC = AD4003BCPZ-RL7 18-bit 2 MSps
    def dataConvertTEI0015(self, adcByteList, adcSamples, adcSignalVolt, adcSignalFloatNormalized, adcSignedInteger):
        for adcSingleValue in range(0, adcSamples):
            adcSingleValue = ((adcSingleValue)*5) # 5 nibble = 20 > 18 bit
            # ADC resolution is 18bit, positive values reach from 0 to 131071, 
            # negatives values from 131072 to 262142        
            adcIntRaw = int(adcByteList[adcSingleValue:adcSingleValue+5], 16)
            if adcIntRaw > 131071:
                adcIntRaw = int(adcIntRaw - 262142)
            adcSignalVolt.append(float(adcIntRaw)*(2*4.096*1/0.4)/262142)
            adcSignalFloatNormalized.append(adcIntRaw/131071)
            adcSignedInteger.append(adcIntRaw)
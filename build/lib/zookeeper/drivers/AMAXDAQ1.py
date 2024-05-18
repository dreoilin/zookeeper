# from .SCPI.VISA_Instrument import VISA_Instrument
import logging
import serial
import numpy as np

config = {
    2 : {
        'Fs' : 2000000,
        'board' : "TEI0015 - 2 MS",
        'AdcMaxInt' : 131072,
        'maxIntThreshold' : 20
    },
    1 : {
        'Fs' : 500000,
        'board' : "TEI0016A - 0.5 MS",
        'AdcMaxInt' : 32768,
        'maxIntThreshold' : 5
    },
    0 : {
        'Fs' : 1000000,
        'board' : "TEI0016B - 1 MS",
        'AdcMaxInt' : 32768,
        'maxIntThreshold' : 5
    }
}

class AMAXDAQ1():
    def __init__(self, port = None, fsample = 115200):
        # serial port e.g '/dev/ttyUSB0'
        self.comport = port 
        self.fsample = fsample
        logging.info("AMAXDAQ1: Successfully instanciated")
        self.__gain = 1
        self.gain = self.__gain
        self.__setup()

    def __setup(self):
        mID = self.ModuleID
        self.config = config[mID-1]
    
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

    @property
    def ModuleID(self):
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

    @property
    def gain(self):
        return self.__gain

    @gain.setter
    def gain(self, gain):
        
        try:
            self.sendCommand(str(gain))
            moduleAdcLinearGain = int(gain)
            # Define plot limits acording to the gain
            plotSignalScale = 10 / moduleAdcLinearGain
            logging.info("Set ADC gain to " + str(moduleAdcLinearGain) 
                        + " or Measurement range to +/- " + str(plotSignalScale) + " V")
            self.__gain = gain
        except:
            logging.info("Error setting gain")

    def acquire(self, N_SAMPLES = 1024):
        # sample length in kS
        if N_SAMPLES not in ['16', '32', '64', '128', '256', '512', '1024']:
            logging.info(f"Invalid N_SAMPLES: {N_SAMPLES} kS")
            return None
        try:# Prevent printing into the text field
            # Collect  adc data and convert to voltage
            adcSignals = self.dataCollect(N_SAMPLES, self.ModuleID)
            
            # Process data for plotting, convert from samples to Milli Seconds
            adcSignalslength = len(adcSignals[0])
            T = 1000 * 1 / self.config['Fs']
            duration = np.arange(0, adcSignalslength * T, T)
            # Scale the signal acording to the gain
            adcSignals[0][:] = [x / self.gain for x in adcSignals[0]]
            # Plot the adc voltage data
            logging.info("Data captured")
            
            # Check if measurment limits are exceeded
            adcLimitsExceeded = signalLimitsExceed(adcSignals[2], moduleAdcMaxAbsThreshold)
            if adcLimitsExceeded > 10:
                text = 'WARNING - ' + str(adcLimitsExceeded) + ' samples exceed measurement range'
                logging.warning("WARNING - INPUTSIGNAL EXCEDDS MEASURMENT LIMITS !")
            
            return adcSignals
        
        except:
            logging.error("Runtime error performing adc data collection")

def signalLimitsExceed(signal, maxAbsValue):
    exceedCounter = 0
    
    for element in signal:
        if abs(element) > maxAbsValue:
            exceedCounter += 1
    return exceedCounter
import time
import numpy as np
from threading import Thread
import Adafruit_MCP4725


class dacThreadSquare:
    def __init__(self,address,dutys = 0.1):
        self.i2caddress = address
        self.interrupt = False
        self.dac = Adafruit_MCP4725.MCP4725(self.i2caddress)
        self.dut = True
        self.dutys = dutys
        
    def start(self):
        print('Starting DAC Thread')
        Thread(target = self.squarewave, args = ()).start()
    
    def squarewave(self):
		
		while True:
			
			if(self.interrupt):
				return
			
			else:	
				if(self.dut == True):
					self.dut = False
					self.dac.set_voltage(4096,True)
					time.sleep(self.dutys)
				else:
					self.dut = True
					self.dac.set_voltage(0,True)
					time.sleep(self.dutys)
    
    def updateDutyCycle(self,val):
		self.dutys = val
		
    def stop(self):
        self.interrupt = True

if __name__ == "__main__":
    #python '/home/pi/Documents/PythonProjects/DAC/simptest.py'
    dac1 = dacThread(0x63)
    
    dac2 = dacThread(0x62)
    
    dac1.start()
    time.sleep(1.5)
    dac2.start()
    
    """
    print('Press Ctrl-C to quit...')
    dut = True
    while True:
        #valueset(int(input('Value is: ')))
        #squarewave(0.1,dut)
        
        dac1
        
        if(dut == True):
            dut = False
        else:
            dut = True
    """

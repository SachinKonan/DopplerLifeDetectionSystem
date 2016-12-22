import time
import numpy as np
from threading import Thread
import Adafruit_MCP4725

class dacThreadTriangle:
	
    def __init__(self,address):
        self.i2caddress = address
        self.interrupt = False
        self.dac1 = Adafruit_MCP4725.MCP4725(self.i2caddress)
            
    def start(self):
        print('Starting DAC Thread')
        Thread(target = self.triwave, args = ()).start()
    
    def triwave(self):
		
		while True:
			
			if(self.interrupt):
				return
			
			else:	
				for i in range(0, 2):
					for x in range(0, 4096):
						if( i == 0):
							val = x
						elif(i == 1):
							val = 4096 - x
						self.dac1.set_voltage(val,True)
    
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

import time
import numpy as np
from threading import Thread
import Adafruit_MCP4725
        
def valueset(val):
    if(val >= 0 and val <= 4096):
        dac.set_voltage(val,True)
        
class dacThreadVAL:
    def __init__(self,address):
        self.i2caddress = address
        self.interrupt = False
        self.dac = Adafruit_MCP4725.MCP4725(self.i2caddress)
        self.val = 0
        
    def start(self):
        print('Starting DAC Thread')
        Thread(target = self.valueset, args = ()).start()
        
    def valueset(self):
		
		while True:
			
			if(self.interrupt):
				return
			
			else:
				if(self.val >= 0 and self.val <= 4096):
					self.dac.set_voltage(self.val,True)
    
    def updateVal(self,val):
		self.val = val
		
    def stop(self):
        self.interrupt = True
    
        

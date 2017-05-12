import time
import numpy as np
from threading import Thread
import Adafruit_MCP4725

class dacThreadSin:
    def __init__(self,address,frequency = 1):
        self.i2caddress = address
        self.interrupt = False
        self.dac = Adafruit_MCP4725.MCP4725(self.i2caddress)
        self.degree = 0
        self.frequency = frequency
        
    def start(self):
        print('Starting DAC Thread')
        Thread(target = self.cycle, args = ()).start()
        
    def cycle(self):
        while True:
            
            if(self.interrupt):
                return
            
            else:
				radians = (self.degree * np.pi/180)
				val = np.sin(2 * np.pi * self.frequency* np.radians(self.degree)) * 2048 + 2048
				#print(val)
				self.dac.set_voltage(int(round(val)),True)
				self.checkdegree()
				time.sleep(0.1)
    
    def checkdegree(self):
		"""
		if(self.degree > 360):
			self.degree = 0
		else:
			self.degree = self.degree
			"""
		self.degree += 1
		
    def stop(self):
        self.interrupt = True

    
        

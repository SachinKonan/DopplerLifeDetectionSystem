import time
import numpy as np
from sinwave import dacThreadSin
from triwave import dacThreadTriangle
from setvalue import dacThreadVAL

def convertValtoVolt(x):
	return int((x/5) * 4096)


if __name__ == "__main__":
    #/home/pi/Documents/PythonProjects/ScienceFair2016/DAC/simptest.py
    dac1 = dacThreadVAL(0x63)
    dac2 = dacThreadVAL(0x62)
    dac1.start()
    dac2.start()
    
    print('Press Ctrl-C to quit...')
    dut = True
    while True:
		
		mag = int(input('Amplitude is: '))
		
		phase = int(input('Phase is: '))
		
		vq = mag * np.cos(phase * np.pi/180)
		
		vi = mag * np.sin(phase * np.pi /180)
		dac1.updateVal(convertValtoVolt(vi))
		dac2.updateVal(convertValtoVolt(vq))
    
   
        

        

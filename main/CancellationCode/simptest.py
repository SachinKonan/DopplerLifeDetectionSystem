import time
import numpy as np
from setvalue import dacThreadVAL
from ADS import ADCThread

def convertValtoVolt(x):
	return int((x/5.0) * 4096.0)


if __name__ == "__main__":
	#/home/pi/Documents/PythonProjects/ScienceFair2016/DAC/simptest.py
	
	adc = ADCThread()
	dac1 = dacThreadVAL(0x63)
	dac2 = dacThreadVAL(0x62)
	dac1.start()
	dac2.start()
	
	time.sleep(1)
	print('Press Ctrl-C to quit...')
	dut = True
	#gain = 0.316
	#dac1.updateVal(convertValtoVolt(2.5))
	#dac2.updateVal(convertValtoVolt(2.5))
	"""
	for x in range(0, 361, 10):
		a = gain/20
		b = 0.316/20
			
		G = 10**a
		Gmax = 10**b
		vi = 1.5 + 1.0 * (G/Gmax) * np.cos(x * np.pi/180)
		vq = 1.5 + 1.0 * (G/Gmax) * np.sin(x * np.pi/180)
		print("At phase: " + str(x))
		print("At amp; " + str(gain))
		
		print("Voltage I " + str(round(vi,4)))
		print("Voltage Q " + str(round(vq,4)))
		dac1.updateVal(convertValtoVolt(vi))
		dac2.updateVal(convertValtoVolt(vq))
		
		time.sleep(1)
		"""
	phase = 45
	gain = 0
	
	while(gain <= 1):
		a = gain/20
		b = 0.316/20
			
		G = gain
		Gmax = 1
		vi = 1.5 + 1.0 * (G/Gmax) * np.cos(phase * np.pi/180)
		vq = 1.5 + 1.0 * (G/Gmax) * np.sin(phase * np.pi/180)
		print("At phase: " + str(phase))
		print("At amp; " + str(gain))
		
		print("Vi " + str(round(vi,4)))
		print("Vq " + str(round(vq,4)))
		dac1.updateVal(convertValtoVolt(vi))
		dac2.updateVal(convertValtoVolt(vq))
		
		gain += 0.05
		time.sleep(1)
		
		
	
	dac1.stop()
	dac2.stop()
		
		
	
   
		

		

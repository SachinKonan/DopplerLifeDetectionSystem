from ADC import ADCThread
from sinwave import dacThreadSin
import time


if __name__ == "__main__":
	# path: /home/pi/Documents/PythonProjects/ScienceFair2016/ADC
	#run: python simptest.py
	adc = ADCThread(address= 0x48, gain = 2/3)
	dac1 = dacThreadSin(0x63)
	dac2 = dacThreadSin(0x62)
	samples = 0
	
	dac1.start()
	
	time.sleep(1)
	
	dac2.start()
	
	adc.start()
	
	start = time.time()
	
	while True:
		print('%d , %d , %d , %d ' % (adc.getADCVal1(),adc.getADCVal2(),adc.getADCVal3(),adc.getADCVal4()))
		samples+=1
	
	end = time.time()
	tottime = end - start
	print('Sampling Rate = %d' % (1000/tottime))

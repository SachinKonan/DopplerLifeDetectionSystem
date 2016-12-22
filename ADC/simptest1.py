from ADC import ADCThread
from sinwave import dacThreadSin
import time
from setvalue import dacThreadVAL

def convertnum(x):
	return (x * 1.0/32767*1.0) * 6.144
	
#max bit val from channel is : 32767
if __name__ == "__main__":
	# path: /home/pi/Documents/PythonProjects/ScienceFair2016/ADC
	#run: python simptest.py
	adc = ADCThread(address= 0x48, gain = 2/3)
	
	dac1 = dacThreadSin(0x63)
	dac2 = dacThreadSin(0x62)
	samples = 0
	
	
	#f = open("data.txt", "w")
	
	dac1.start()
	
	time.sleep(1)
	
	dac2.start()
	
	adc.start()
	
	#dac2.updateVal(4096)
	
	
	time.sleep(1)
	start = time.time()
	samples = 0
	tot = 0
	while samples < 1000:
		val = round(convertnum(adc.getADCVal4()),5)
		samples +=1
		str1 = str(val)
		
		tot = val + tot
		
		print(str1 + '            ' + 'AVERAGE IS: ' + str(tot/samples))
		#print('%d , %d , %d , %d ' % (,adc.getADCVal2(),adc.getADCVal3(),adc.getADCVal4()))
		time.sleep(0.1)
	
	adc.stop()
	dac1.stop()
	dac2.stop()
	
	end = time.time()
	tottime = end - start
	print('Sampling Rate = %d' % (1000/tottime))
		
	

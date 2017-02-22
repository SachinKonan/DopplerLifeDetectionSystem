from setvalue import dacThreadVAL
from ADS import ADCThread
import time
def getValue(fatval):
	dac2.updateVal(fatval)
	time.sleep(0.13)
	ret = adc.getADCVAL(1)
	print(ret)
	return ret 

	
dac1 = dacThreadVAL(address=0x63)
dac2 = dacThreadVAL(address = 0x62)
adc = ADCThread(address = 0x48)

dac1.start()
dac2.start()
adc.start()

increment = 0
ABSVAL = 2.5
error = 0
simpval = int((ABSVAL/3.3) * 4096)
origin = simpval
returned = 0
i = 0

returned = getValue(simpval)

error = returned - ABSVAL
while(abs(error) > 0.001 and i <=200):
	#print('Error is: %s' % error)
	if(returned < ABSVAL):
		simpval+=1
	elif(returned > ABSVAL):
		simpval-=1
	print(simpval)	
	returned = getValue(simpval)
	print(returned)
	error = returned - ABSVAL
	i+=1

print(simpval - origin)


dac1.stop()
dac2.stop()
adc.stop()



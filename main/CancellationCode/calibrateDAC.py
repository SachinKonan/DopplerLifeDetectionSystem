from setvalue import dacThreadVAL
from ADS import ADCThread

dac1 = dacThreadVAL(address=0x63)
dac2 = dacThreadVAL(address = 0x62)
adc = ADCThread(address = 0x48)

dac1.start()
dac2.start()
adc.start()

ABSVAL = 2.5
error = 0
simpval = int((2.5/3.3) * 4096)
returned = 0
i = 0

getValue()

error = returned - ABSVAL
while(abs(error) > 0.009 and i <=50):
    if(error < ABSVAL):
        simpval+=1
    elif(error > ABSVAL):
        simpval-=1
    getValue()
    error = returned - ABSVAL
    i+=1



def getValue():
    dac1.updateVal(simpval)
    time.sleep(0.1)
    returned = adc.getADCVAL(0)

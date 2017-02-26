import matplotlib.pyplot as plt
import numpy as np
from ADS import ADCThread
from setvalue import dacThreadVAL
tot_size = 3120
steps = 20
increment = int(tot_size/steps)

low = 200
holder = [0,0, low]
adc = ADCThread(0x48)
dac1 = dacThreadVAL(0x63)
dac2 = dacThreadVAL(0x62)

adc.start()
dac1.start()
dac2.start()

for i in range(0, tot_size,increment):
    for q in range(0, tot_size,increment):
        #add dac stuff
        dac1.updateVal(i)
        dac2.updateVal(q)
        time.sleep(0.08)
        val = adc.getADCVAL(0)
        if(val < holder[2]):
            holder[0] = i
            holder[1] = q
            holder[2] = val

#print('\n')

print('Lowest Val is at I: %s and Q: %s' %(holder[0],holder[2]))

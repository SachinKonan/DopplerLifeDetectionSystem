import matplotlib.pyplot as plt
import numpy as np
from ADS import ADCThread
from setvalue import dacThreadVAL
import time

tot_size = 3120
steps = 20
increment = int(tot_size/steps)

low = 200
holder = [0,0, low]
adc = ADCThread(0x48)
dac1 = dacThreadVAL(0x63)
dac2 = dacThreadVAL(0x62)

adc.start()
print('Starting ADC')
dac1.start()
dac2.start()
print('Press Control-C To stop')

phaselist = []
gainlist = []
voltlist = []
for i in range(0, tot_size+1,increment):
    for q in range(0, tot_size+1,increment):
        #add dac stuff
        dac1.updateVal(i)
        dac2.updateVal(q)
        time.sleep(0.08)
        val = adc.getADCVAL(0)
        if(val < holder[2]):
            holder[0] = i
            holder[1] = q
            holder[2] = val
        phaselist.append(i)
        gainlist.append(q)
        voltlist.append(val)
        print('At I Val: %s and Q Val: %s, OUTPUT: %s' %(i,q,val))


#print('\n')
print('Lowest Val is at I: %s and Q: %s' %(holder[0],holder[1]))

plt.plot(phaselist, voltlist)

plt.show()

plt.plot(gainlist, voltlist)

plt.show()

adc.stop()
dac1.stop()
dac2.stop()

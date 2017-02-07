import matplotlib.pyplot as plt
import numpy as np
import time

MAX_GAIN = 0.316
gain = -40
phase = 30
keyvals= [10,10]

xvals = []
yvals = []

while gain <= 0.316:
    a = gain/20
    b = MAX_GAIN/20

    G = 10**a
    Gmax = 10**b
    vi = 1.5 + 1.0 * (G/Gmax) * np.cos(phase * np.pi/180)
    vq = 1.5 + 1.0 * (G/Gmax) * np.sin(phase * np.pi/180)

    val = np.random.rand() * 5
    if(val  < keyvals[1]):
        keyvals[0] = gain
        keyvals[1] = val

    print('At amp: %s'%(gain))
    print('I Bit Equivalent: %s' %(int((vi/3.3) * 4096)))
    print('Q Bit Equivalent: %s'% (int((vq/3.3) * 4096)))
    print('XXXXXXXXXXXXXX')
    time.sleep(1.5)
    gain +=0.8

import matplotlib.pyplot as plt
import numpy as np


time = np.arange(0, 10,0.02)

plt.ion()

for phase in range(0, 360,10):
    plt.ylim(-7,7)
    vco = np.sin(2 * np.pi * time + 45 * np.pi/180)
    vector = np.sin(2 * np.pi * time + phase* np.pi/180)

    sum1 = (vco + vector)
    realsum = vco*(3 * vco + vector)
    #plt.plot(time,vco)
    plt.plot(time,sum1)
    plt.plot(time, realsum)

    plt.pause(0.01)
    plt.draw()
    plt.clf()

plt.close()

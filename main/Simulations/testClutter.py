import matplotlib.pyplot as plt
import numpy as np


time = np.arange(0, 10,0.02)

plt.ion()

for phase in range(0, 720,10):
    plt.ylim(0,400)
    plt.title('Radar Simulation')

    vco = 6*np.sin(2 * np.pi * time + 40 * np.pi/180)
    LOintermediate = vco -3
    rfout = vco -3

    LO = LOintermediate -3
    cancel = LOintermediate -3

    vector = np.sin(2 * np.pi * time + phase * np.pi/180) - 10
    visualizer = 6*np.sin(2 * np.pi * time + phase * np.pi/180) -3 + rfout

    adder = vector + rfout

    mixer = LO * adder

    plt.plot(time, mixer,'-b',label='mixer = LO *(vector + rfin)')
    plt.plot(time,visualizer,'-r',label = 'vector + rfin')

    plt.legend(loc='upper right')
    plt.pause(0.01)
    plt.draw()
    plt.clf()

plt.close()

import matplotlib.pyplot as plt
import numpy as np


time = np.arange(0, 10,0.002)
frequency = 2.4 * (10**9)
print(frequency )
plt.ion()

for phase in range(0, 720,10):
    plt.ylim(-10,10)
    plt.title('Radar Simulation')

    vco = 6*np.sin(2 * np.pi * time * frequency + 40 * np.pi/180)
    LOintermediate = 3*np.sin(2 * np.pi * time * frequency + 40 * np.pi/180)
    rfout = 3*np.sin(2 * np.pi * time * frequency + 40 * np.pi/180)

    LO = np.sin(2 * np.pi * time * frequency + 40 * np.pi/180)
    cancel = np.sin(2 * np.pi * time * frequency + 40 * np.pi/180)

    # 1- 10 for 10 dB attenuation from modulator at max gain setting

    vector = (1-10)*np.sin(2 * np.pi * time * frequency + phase * np.pi/180) - 10
    visualizer = 3*np.sin(2 * np.pi * time * frequency+ phase * np.pi/180) + rfout
    # i am using this to visualize the degree of cancellation between the modulator and the rf input
    adder = vector + rfout

    mixer = LO * adder

    plt.plot(time, mixer,'-b',label='mixer = LO *(vector + rfin)')
    plt.plot(time,visualizer,'-r',label = 'vector + rfin')

    plt.legend(loc='upper right')
    plt.pause(0.01)
    plt.draw()
    plt.clf()

plt.close()

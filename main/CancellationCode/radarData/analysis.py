import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.fftpack import fft

string = 'test1.npy'

radarData = np.load(string)

plt.plot(radarData)
plt.show()

yf = fft(radarData)
return xf, abs(yf[0:self.nfft / 2])
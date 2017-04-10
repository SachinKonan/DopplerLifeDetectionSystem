import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.fftpack import fft
from scipy.signal import butter, lfilter, freqz

string = 'radarData\\testpri1.npy'
stringnoise = 'radarData\\testpribaseline.npy'
signal = np.load(string)
data1 = np.load(stringnoise)

#data = signal[800:1050]
#noise = data1[800: 1050]

data = signal[800-250:1050-250]*0.6
noise = data1[500: 750]

plt.plot(data, linewidth = 3,label='Signal')
plt.plot(noise,linewidth = 3, label = 'Control')
plt.title('PCA Selected Brick Sample T1 (After filter and Window)')
plt.xlabel('Samples')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid()
plt.show()


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

newData1 = butter_lowpass_filter(data=data, cutoff =2, fs= 75)
newData2 = butter_lowpass_filter(data=noise, cutoff =2, fs= 75)

N = len(data)
# sample spacing
T = 1.0 / 75
x = np.linspace(0.0, N*T, N)
y = newData1
yf = fft(y)
ynoise = fft(newData2)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

yf = 2.0/N * np.abs(yf[:N//2])
ynoise = 2.0/N * np.abs(ynoise[:N//2])

plt.plot(xf, yf, linewidth=3, label='Signal')
plt.plot(xf, ynoise, linewidth=3, label = 'Control')
plt.legend()
plt.xlim((0, 20))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.title('Brick FFT')
plt.grid()
plt.show()

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

vnrrat = sum(ynoise[1:find_nearest(xf, 3.3)])
vnrratsig = sum(yf[1:find_nearest(xf, 3.3)])

print(vnrratsig)
print(vnrrat)

"""
noise = np.random.normal(0,0.002,2500)

plt.plot(noise)
plt.title('Control for Concrete Test')
plt.xlabel('Samples')
plt.ylabel('Voltage')
plt.show()

N = len(noise)
# sample spacing
T = 1.0 / 200
x = np.linspace(0.0, N*T, N)
y = noise
yf = fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

yf = yf * 0.5
plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.title('Concrete Control FFT')
plt.grid()
plt.show()


radarData = np.load(string)

radarData1 = radarData[0: 450]

radarData2 = radarData[450: 900]

radarData3 = radarData[900: 1350]

radarData4 = radarData[1350: 1350 + 450]

radarData5 = radarData[1350 + 450 : 1350 + 450 *2]

radarData6 = radarData[1350 + 450*2 : 1350 + 450 *3]
plt.plot(radarData1)
plt.xlabel('Samples')
plt.ylabel('Voltage')
plt.title('Control Brick 1 Test')
plt.grid()
plt.show()

plt.plot(radarData2)
plt.xlabel('Samples')
plt.ylabel('Voltage')
plt.title('Control Brick 2 Test')
plt.grid()
plt.show()

plt.plot(radarData3)
plt.xlabel('Samples')
plt.ylabel('Voltage')
plt.title('Control Brick 3 Test')
plt.grid()
plt.show()


plt.plot(radarData1)
plt.xlabel('Samples')
plt.ylabel('Voltage')
plt.title('Control Concrete 1 Test')
plt.grid()
plt.show()

plt.plot(radarData2)
plt.xlabel('Samples')
plt.ylabel('Voltage')
plt.title('Control Concrete 2 Test')
plt.grid()
plt.show()

plt.plot(radarData3)
plt.xlabel('Samples')
plt.ylabel('Voltage')
plt.title('Control Concrete 3 Test')
plt.grid()
plt.show()

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
newData1 = butter_lowpass_filter(data=radarData1, cutoff =2, fs= 200)
newData2 = butter_lowpass_filter(data=radarData2, cutoff =2, fs= 200)
newData3 = butter_lowpass_filter(data=radarData3, cutoff =2, fs= 200)

newData = butter_lowpass_filter(data=radarData, cutoff = 2, fs= 200)
plt.plot(newData1)
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.title('PCA Selected Filtered Data')
plt.grid()
plt.show()

plt.plot(newData2)
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.title('PCA Selected Filtered Data')
plt.grid()
plt.show()

plt.plot(newData3)
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.title('PCA Selected Filtered Data')
plt.grid()
plt.show()


N = len(noise)
# sample spacing
T = 1.0 / 200
x = np.linspace(0.0, N*T, N)
y = noise
yf = fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))
plt.xlim((0, 20))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.title('Control Concrete Test')
plt.grid()
plt.show()
"""
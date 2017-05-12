import tkinter as tk
from tkinter import ttk
from tkinter import Entry
import matplotlib
import matplotlib.pylab as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
import numpy as np
import time
import sys
from threading import Thread
import tkinter.simpledialog as simpledialog
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.linalg import hankel
from scipy.signal import butter, lfilter, freqz
from PIL import Image, ImageTk

matplotlib.use("TkAgg")

large_font = ("Verdana", 12)
small_font = ("Verdana", 8)

# phasedac = dacThreadVAL(0x63).start()
# ampdac = dacThreadVAL(0x62).start()
# adc = ADCThread().start()

def convertValtoVolt(x):
    return int((x / 3.3) * 4096.0)

isOn = True

class MainGui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=large_font)
        label.pack(pady=10, padx=10)

        button3 = ttk.Button(self, text="Visit Oscilloscope", command=lambda: controller.show_frame(PageThree))
        button3.pack()

        #this will have to be changed based on user file location
        im = Image.open("C:\\Users\\Sachin Konan\\Documents\\DopplerLifeDetectionSystem\\main\\SimpleOscilloscope\\RPIVisulaization.png")
        photo = ImageTk.PhotoImage(im)

        self.labelImage = tk.Label(self, image=photo)
        self.labelImage.image = photo  # keep a reference!
        self.labelImage.pack()


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        label = tk.Label(self, text="Oscilloscope", font=large_font)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: self.pageChanger())
        button1.pack()

        self.channel = 0
        self.label5 = tk.Label(self, text="Current Channel: " + str(self.channel), font=small_font)
        self.label5.pack(side=tk.BOTTOM)

        self.phase = tk.Scale(self, label="DAC1 :", from_=0, to=4096, sliderlength=20, length=400, orient=tk.HORIZONTAL)
        self.amplitude = tk.Scale(self, label="DAC2 :", from_=0, to=4096, sliderlength=20, length=400,
                                  orient=tk.HORIZONTAL)

        self.phase.pack(side=tk.TOP, padx=2, pady=5)
        self.amplitude.pack(side=tk.TOP, padx=2, pady=5)

        frame = tk.Frame(self)
        frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        chan1 = ttk.Button(frame, text="Channel 0", command=lambda: self.add(0))
        chan1.pack(pady=35, padx=20)
        chan2 = ttk.Button(frame, text="Channel 1", command=lambda: self.add(1))
        chan2.pack(pady=35, padx=20)
        chan3 = ttk.Button(frame, text="Channel 2", command=lambda: self.add(2))
        chan3.pack(pady=35, padx=20)
        chan4 = ttk.Button(frame, text="Channel 3", command=lambda: self.add(3))
        chan4.pack(pady=35, padx=20)

        f = Figure(figsize=(6, 4), dpi=100)
        self.ax = f.add_subplot(111)
        self.ax.grid(True)

        xAchse = np.arange(0, 100, 1)
        yAchse = np.array([0] * 100)

        self.ax.grid(True)
        self.ax.set_title("Realtime Waveform Plot")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Amplitude")
        self.ax.axis([0, 100, -5, 5])
        self.line1 = self.ax.plot(xAchse, yAchse, '-')

        self.canvas = FigureCanvasTkAgg(f, master=self)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.values = [0 for x in range(100)]

        self.thread = Thread(target=self.SinwaveformGenerator, args=())
        self.thread.start()
        self.thread1 = Thread(target=self.RealtimePlotter, args=())
        self.thread1.start()

    def pageChanger(self):
        self.controller.show_frame(StartPage)
        self.thread.join()
        self.thread1.join()

    def add(self, var):
        self.channel = var
        self.label5["text"] = "Current Channel is " + str(self.channel)

    def controlDACPhase(self):
        # print(self.phase.get())

        valstring = str(self.phase.get())

        try:
            val = float(valstring)

        # phasedac.updateVal(val)
        except ValueError:
            print("cant convert")
        self.update()

    def controlDACAmp(self):

        valstring = str(self.amplitude.get())

        try:
            val = float(valstring)
        # ampdac.updateVal(val)
        except ValueError:
            print("can't convert")
        self.update()

    def SinwaveformGenerator(self):

        # add adc stuff here
        # self.values.append(adc.getADCVAL(self.channel))
        self.controlDACPhase()
        self.controlDACAmp()
        self.values.append(np.random.rand() * 2 - 1)
        self.after(ms=25, func=self.SinwaveformGenerator)

    def RealtimePlotter(self):
        CurrentXAxis = np.arange(len(self.values) - 100, len(self.values), 1)
        self.line1[0].set_data(CurrentXAxis, np.array(self.values[-100:]))
        self.ax.axis([CurrentXAxis.min(), CurrentXAxis.max(), -5, 5])
        self.canvas.draw()
        self.after(ms=25, func=self.RealtimePlotter)

    def converttoVolt(x):
        return (x / 4096) * 3.3

class Radar(object):
    def __init__(self, radar, samplingRate):
        self.radar = [radar[i][0] for i in range(0, len(radar))]
        self.time = [radar[i][1] for i in range(0, len(radar))]
        self.samplingRate = samplingRate
        self.p = 5
        self.nfft = 512
        self.list = []
        self.cutoff = 2
        self.radarobj = None
        self.order = 6
    def getVariables(self):
        return self.samplingRate, self.radar, self.time

    def main(self):
        radar, time = self.slidingwindow()
        fft = self.fft(radar)
        peakY = np.max(fft[1])  # Find max peak
        locY = fft[0][np.argmax(fft[1])]  # Find its location
        return {
            'fft': fft,
            'peak': peakY,
            'loc': locY
        }

    def slidingwindow(self):

        if (len(self.radar) == 2500):
            overlap = 0.4

            nw = 250
            ns = int(nw * (1.0 - overlap))
            n0 = 0
            n1 = n0 + nw
            N = len(self.radar)

            counter = 0
            counter1 = 1

            SNR = 0
            bestwin = 0
            besttime = 0
            while True:
                data = self.radar[n0:n1]
                time = self.time[n0:n1]
                array = Radar.HanningFunction(data)
                filtered_data = Radar.butter_lowpass_filter(array, self.cutoff, self.samplingRate, order=self.order)
                corrMtrx = self.getcorrMtrx(x=filtered_data, m=35)
                frequency, psd, eigenvals = self.musicAlg(corrMtrx)
                currSNR = sum(eigenvals[0:self.p])/ sum(eigenvals[self.p: len(eigenvals)])
                if(currSNR > SNR ):
                    SNR = currSNR
                    bestwin = filtered_data
                    besttime = time
                #r = counter // n
                #c = counter % n
                #ax[r][c].plot(eigenvals)
                #ax[r][c + 1].plot(xf, yf)
                n0 += ns
                n1 += ns
                counter += 2
                counter1 += 1
                if n1 > N:
                    break

            return bestwin, besttime
        else:
            print("Error your data vector is not the proper length")

    def diffCalc(self, list1):
        list2 = []
        for i in range(1, len(list1)):
            list2.append(list1[i] - list1[i - 1])
        return list2

    def fft(self, array):
        yf = fft(array, n=self.nfft)
        xf = np.linspace(0.0, self.samplingRate / 2, self.nfft / 2)
        return xf, abs(yf[0:self.nfft / 2])

    def HanningFunction(radarData):
        return radarData * np.hanning(len(radarData))

    def getcorrMtrx(self, x, m):
        x = np.array(x)
        m = m
        N = len(x)
        xlen = m + 1
        rowVector = x[N - xlen: N]
        columnVector = x[0: N - m]
        hanMatrix = hankel(c=np.array(columnVector).T, r=rowVector)
        X_unscaled = np.fliplr(hanMatrix)
        X = X_unscaled / np.sqrt(N - m)
        Xnew = np.conj(np.fliplr(X))
        corrMatrix = np.vstack((X, Xnew)) / np.sqrt(2)
        return corrMatrix

    def musicAlg(self,corrMtrx):
        u, s, v = np.linalg.svd(corrMtrx)

        self.nfft = 512

        frequencyVector = np.linspace(0, 1, self.nfft // 2)
        frequencyVector *= self.samplingRate / 2

        sum = 0
        for i in range(self.p, len(v)):
            y = fft(v[i], n=self.nfft)
            sum += abs(y) ** 2 / s[i]

        sum = 1 / sum

        sum = sum[0:self.nfft // 2]

        return frequencyVector, sum, s

    def graphFilterResults(self):
        order = 6
        cutoff = 2

        b, a = Radar.butter_lowpass(cutoff, self.samplingRate, order)

        w, h = freqz(b, a, worN=8000)
        plt.subplot(2, 1, 1)
        plt.plot(0.5 * fs * w / np.pi, np.abs(h), 'b')
        plt.plot(cutoff, 0.5 * np.sqrt(2), 'ko')
        plt.axvline(cutoff, color='k')
        plt.xlim(0, 0.5 * fs)
        plt.title("Lowpass Filter Frequency Response")
        plt.xlabel('Frequency [Hz]')
        plt.grid()

        y = Radar.butter_lowpass_filter(self.radar, cutoff, fs, order)

        plt.subplot(2, 1, 2)
        plt.plot(self.time, self.radar, 'b-', label='data')
        plt.plot(self.time, y, 'g-', linewidth=2, label='filtered data')
        plt.xlabel('Time [sec]')
        plt.grid()
        plt.legend()

        plt.subplots_adjust(hspace=0.35)
        plt.show()
        return y

    def butter_lowpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(data, cutoff, fs, order=5):
        b, a = Radar.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def testSpectrum(self, data):
        corrMtrx = self.getcorrMtrx(data, 30)
        return self.musicAlg2(corrMtrx)

    def musicAlg2(self, corrMtrx):
        u, s, v = np.linalg.svd(corrMtrx)

        self.nfft = 512

        frequencyVector = np.linspace(0, 1, self.nfft // 2)
        frequencyVector *= self.samplingRate / 2

        sum = 0
        for i in range(self.p, len(v)):
            y = fft(v[i], n=self.nfft)
            sum += abs(y) ** 2 / s[i]

        sum = 1 / sum

        sum = sum[0:self.nfft // 2]

        return frequencyVector, sum, s

def on_closing():
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()
    else:
        isOn = True

app = MainGui()
app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()

# phasedac.stop()
# ampdac.stop()
# adc.stop()

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
from setvalue import dacThreadVAL
from ADS import ADCThread

style.use("ggplot")

matplotlib.use("TkAgg")

large_font = ("Verdana", 12)
small_font = ("Verdana", 8)

phasedac = dacThreadVAL(0x63).start()
ampdac = dacThreadVAL(0x62).start()

adc = ADCThread().start()

class MainGui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

def qf(sting):
    print(sting)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Start Page", font = large_font)
        label.pack(pady = 10, padx = 10)

        button1 = ttk.Button(self, text = "Visit Page 1", command=lambda:controller.show_frame(PageOne))
        button1.pack()
        button2 = ttk.Button(self, text = "Visit Page 2", command=lambda:controller.show_frame(PageTwo))
        button2.pack()
        button3 = ttk.Button(self, text = "Visit Oscilloscope", command=lambda:controller.show_frame(PageThree))
        button3.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Page one", font = large_font)
        label.pack(pady = 10, padx = 10)

        button = ttk.Button(self, text = "Back to Home", command=lambda:controller.show_frame(StartPage))
        button.pack()
        button1 = ttk.Button(self, text = "Page Two", command=lambda:controller.show_frame(PageTwo))
        button1.pack()

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Page Two", font = large_font)
        label.pack(pady = 10, padx = 10)

        button1 = ttk.Button(self, text = "Back to Home", command=lambda:controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text = "Page one", command=lambda:controller.show_frame(PageOne))
        button2.pack()

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.controller = controller
        label = tk.Label(self,text = "Oscilloscope", font = large_font)
        label.pack(pady = 10, padx = 10)

        button1 = ttk.Button(self, text = "Back to Home", command= lambda:self.pageChanger())
        button1.pack()

        self.channel = 0
        self.label5 = tk.Label(self,text = "Current Channel: " + str(self.channel), font=small_font)
        self.label5.pack(side=tk.BOTTOM)

        self.phase = tk.Scale(self,label="DAC1 :", from_=0, to=4096,sliderlength=20, length=400,orient=tk.HORIZONTAL)
        self.amplitude = tk.Scale(self,label="DAC2 :", from_=0, to=4096,sliderlength=20, length= 400,orient=tk.HORIZONTAL)

        self.phase.pack(side=tk.TOP,padx=2,pady=5)
        self.amplitude.pack(side=tk.TOP,padx=2,pady=5)

        frame = tk.Frame(self)
        frame.pack(side = tk.RIGHT, fill = tk.BOTH)

        chan1 = ttk.Button(frame, text = "Channel 0", command= lambda: self.add(0))
        chan1.pack(pady = 35, padx = 20)
        chan2 = ttk.Button(frame, text = "Channel 1", command=  lambda: self.add(1))
        chan2.pack(pady = 35, padx = 20)
        chan3 = ttk.Button(frame, text = "Channel 2", command=  lambda: self.add(2))
        chan3.pack(pady = 35, padx = 20)
        chan4 = ttk.Button(frame, text = "Channel 3", command=  lambda: self.add(3))
        chan4.pack(pady = 35, padx = 20 )



        f = Figure(figsize = (5,4), dpi = 100)
        self.ax = f.add_subplot(111)
        self.ax.grid(True)


        xAchse=plt.arange(0,100,1)
        yAchse=plt.array([0]*100)

        self.ax.grid(True)
        self.ax.set_title("Realtime Waveform Plot")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Amplitude")
        self.ax.axis([0,100,-5,5])
        self.line1= self.ax.plot(xAchse,yAchse,'-')

        self.canvas = FigureCanvasTkAgg(f,master=self)
        self.canvas.get_tk_widget().pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        self.values = [0 for x in range(100)]

        #self.after(ms=100, func=self.SinwaveformGenerator)
        #self.after(ms=100, func=self.RealtimePlotter)

        self.thread = Thread(target=self.SinwaveformGenerator,args=())
        self.thread.start()

        self.thread1 = Thread(target = self.RealtimePlotter, args=())
        self.thread1.start()

    def pageChanger(self):
        self.controller.show_frame(StartPage)
        self.thread.join()
        self.thread1.join()

    def add(self,var):
        self.channel = var
        self.label5["text"] = "Current Channel is " + str(self.channel)


    def controlDACPhase(self):
        #print(self.phase.get())

        valstring = str(self.phase.get())

        try:
            val = int(valstring)
            #print(val)
            phasedac.updateVal(val)
        except ValueError:
            print("cant convert")
        self.update()

    def controlDACAmp(self):

        valstring = str(self.amplitude.get())

        try:
            val = int(valstring)
            #print(val)
            ampdac.updateVal(val)
        except ValueError:
            print("can't convert")
        self.update()

    def SinwaveformGenerator(self):

      #add adc stuff here
      #self.values.append(adc.getADCVAL(self.channel))
      self.controlDACPhase()
      self.controlDACAmp()
      #self.values.append(np.random.rand()*2 -1)
      self.values.append(adc.getADCVAL(self.channel))
      self.after(ms = 25, func= self.SinwaveformGenerator)
      #time.sleep(0.025)
      #self.SinwaveformGenerator()

    def RealtimePlotter(self):
      CurrentXAxis=plt.arange(len(self.values)-100,len(self.values),1)
      self.line1[0].set_data(CurrentXAxis,plt.array(self.values[-100:]))
      self.ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-5,5])
      self.canvas.draw()
      self.after(ms = 25, func= self.RealtimePlotter)

    def converttoVolt(x):
        return (x/4096) * 3.3

app = MainGui()
app.mainloop()

phasedac.stop()
ampdac.stop()
adc.stop()

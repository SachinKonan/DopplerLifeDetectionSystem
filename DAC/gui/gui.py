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

style.use("ggplot")

matplotlib.use("TkAgg")

large_font = ("Verdana", 12)
small_font = ("Verdana", 8)
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
        label = tk.Label(self,text = "Oscilloscope", font = large_font)
        label.pack(pady = 10, padx = 10)

        button1 = ttk.Button(self, text = "Back to Home", command= leavePage(controller))
        button1.pack()

        label1 = tk.Label(self,text = "Phase Setting (0 - 360)", font=small_font)
        label1.pack(side = tk.TOP)

        self.phase = tk.StringVar()
        eBox = tk.Entry(self, textvariable=self.phase)
        eBox.pack(side=tk.TOP)

        buttonphase = ttk.Button(self, text = "Send to DAC1", command=self.controlDACPhase)
        buttonphase.pack(side = tk.TOP)


        #########################

        label1 = tk.Label(self,text = "Amplitude Setting (0.316:-100)", font=small_font)
        label1.pack(side = tk.TOP)

        self.amp = tk.StringVar()
        eBox = tk.Entry(self, textvariable=self.amp)
        eBox.pack(side=tk.TOP)

        buttonamp = ttk.Button(self, text = "Send to DAC2", command=self.controlDACAmp)
        buttonamp.pack(side = tk.TOP)


        self.label3 = tk.Label(self,text = "" + str(self.amp.get()), font=small_font)
        self.label3.pack(side=tk.BOTTOM)
        self.label2 = tk.Label(self,text = "" + str(self.phase.get()), font=small_font)
        self.label2.pack(side=tk.BOTTOM)


        #self.updateGUIVals()

        f = Figure(figsize = (5,3), dpi = 100)
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

        self.SinwaveformGenerator()
        self.RealtimePlotter()

    def controlDACPhase(self):
        #print(self.phase.get())

        valstring = self.phase.get()
        val = float(valstring)

        if(val>= 0 and val <= 360):
            self.label2["text"] = "Current Phase is: " + valstring
            #add dac stuff

        else:
            self.label2["text"] = "Current Phase is: INVALID"
        self.update()

    def controlDACAmp(self):

        valstring = self.amp.get()
        val = float(valstring)

        if(val>= -100 and val <= 0.316):
            self.label3["text"] = "Current Gain is: " + valstring + " dB"
            #add dac stuff here
        else:
            self.label2["text"] = "Current Gain is: INVALID"

        self.update()

    def SinwaveformGenerator(self):

      #add adc stuff here
      self.values.append(np.random.rand()*2 -1)
      self.after(ms = 25, func= self.SinwaveformGenerator)
      #time.sleep(0.025)
      #self.SinwaveformGenerator()

    def RealtimePlotter(self):
      CurrentXAxis=plt.arange(len(self.values)-100,len(self.values),1)
      self.line1[0].set_data(CurrentXAxis,plt.array(self.values[-100:]))
      self.ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-5,5])
      self.canvas.draw()
      self.after(ms = 25, func= self.RealtimePlotter)
def leavePage(controller):
    controller.show_frame(StartPage)
app = MainGui()
app.mainloop()

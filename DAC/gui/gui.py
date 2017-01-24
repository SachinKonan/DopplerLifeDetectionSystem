import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.pylab as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
import numpy as np

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

        button1 = ttk.Button(self, text = "Back to Home", command=lambda:controller.show_frame(StartPage))
        button1.pack()

        label1 = tk.Label(self,text = "Phase Setting (0 - 360)", font=small_font )
        label1.pack()

        self.entrytext = str()
        self.Entry(self.root, textvariable=self.entrytext).pack()




        f = Figure(figsize = (6,4), dpi = 100)
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

        self.after(ms=100, func=self.SinwaveformGenerator)
        self.after(ms=100, func=self.RealtimePlotter)

    def SinwaveformGenerator(self):

      #add adc stuff here
      self.values.append(np.random.rand()*2 -1)
      self.after(ms = 25, func= self.SinwaveformGenerator)

    def RealtimePlotter(self):
      CurrentXAxis=plt.arange(len(self.values)-100,len(self.values),1)
      self.line1[0].set_data(CurrentXAxis,plt.array(self.values[-100:]))
      self.ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-5,5])
      self.canvas.draw()
      self.after(ms = 25, func= self.RealtimePlotter)



app = MainGui()
app.mainloop()

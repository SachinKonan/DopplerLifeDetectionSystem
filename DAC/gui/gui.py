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
from setvalue import dacThreadVAL
import Adafruit_ADS1x15

style.use("ggplot")

matplotlib.use("TkAgg")

large_font = ("Verdana", 12)
small_font = ("Verdana", 8)


phasedac = dacThreadVAL(0x63).start()
ampdac = dacThreadVAL(0x62).start()
		
adc = Adafruit_ADS1x15.ADS1115()

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
		
		button1 = ttk.Button(self, text = "Back to Home", command= lambda: controller.show_frame(StartPage))
		button1.pack()

		label1 = tk.Label(self,text = "Phase Setting (0 - 360)", font=small_font)
		label1.pack(side = tk.TOP)

		self.phase = tk.StringVar()
		eBox = tk.Entry(self, textvariable=self.phase)
		eBox.pack(side=tk.TOP)

		buttonphase = ttk.Button(self, text = "Send to DAC1", command=self.controlDACPhase)
		buttonphase.pack(side = tk.TOP)

		self.label2 = tk.Label(self,text = "Current Phase is: ", font=small_font)
		self.label2.pack(side=tk.TOP)

		#########################

		label3 = tk.Label(self,text = "Amplitude Setting (0.316:-100)", font=small_font)
		label3.pack(side = tk.TOP)

		self.amp = tk.StringVar()
		eBox1 = tk.Entry(self, textvariable=self.amp)
		eBox1.pack(side=tk.TOP)

		buttonamp = ttk.Button(self, text = "Send to DAC2", command=self.controlDACAmp)
		buttonamp.pack(side = tk.TOP)


		self.label4 = tk.Label(self,text = "Current Amplitude: ", font=small_font)
		self.label4.pack(side=tk.TOP)

		#self.updateGUIVals()

		f = Figure(figsize = (6,4), dpi = 100)
		self.ax = f.add_subplot(111)
		self.ax.grid(True)


		xAchse=plt.arange(0,100,1)
		yAchse=plt.array([0]*100)

		self.ax.grid(True)
		self.ax.set_title("Realtime Waveform Plot")
		self.ax.set_xlabel("Time")
		self.ax.set_ylabel("Amplitude")
		self.ax.axis([0,100,-7,7])
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

		try:
			val = float(valstring)

			if(val>= 0 and val <= 360):
				self.label2["text"] = "Current Phase is: " + valstring
				#add dac stuff
				phasedac.updateVal(int((val /3.0) * 4096))

			else:
				self.label2["text"] = "INVALID"
		except ValueError:
			print("cant convert")
		self.update()

	def controlDACAmp(self):

		valstring = self.amp.get()

		try:
			val = float(valstring)

			if(val>= -100 and val <= 3.3):
				self.label4["text"] = "Current Amplitude is: " + valstring
				#add dac stuff here
				ampdac.updateVal(int((val /3.3) * 4096))
			else:
				self.label4["text"] = "INVALID"
		except ValueError:
			print("can't convert")
		self.update()

	def SinwaveformGenerator(self):

	  #add adc stuff here
	  self.values.append((adc.read_adc(0, gain=2/3)/32767.0)* 6.144)
	  #self.values.append(np.random.rand()*2 -1)
	  self.after(ms = 25, func= self.SinwaveformGenerator)
	  #time.sleep(0.025)
	  #self.SinwaveformGenerator()

	def RealtimePlotter(self):
	  CurrentXAxis=plt.arange(len(self.values)-100,len(self.values),1)
	  self.line1[0].set_data(CurrentXAxis,plt.array(self.values[-100:]))
	  self.ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-7,7])
	  self.canvas.draw()
	  self.after(ms = 25, func= self.RealtimePlotter)

app = MainGui()
app.mainloop()

phasedac.stop()
ampdac.stop()
adc.stop()

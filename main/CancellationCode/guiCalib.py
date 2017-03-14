import time
import numpy as np
from setvalue import dacThreadVAL
from ADS import ADCThread
import matplotlib.pylab as plt
import tkinter as tk
from tkinter import ttk
from tkinter import Entry
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
import numpy as np
import time
import sys
from threading import Thread


#style.use("ggplot")

#matplotlib.use("TkAgg")

large_font = ("Verdana", 12)
small_font = ("Verdana", 8)

adc = ADCThread(address=0x48).start()
dac1 = dacThreadVAL(0x63).start()
dac2 = dacThreadVAL(0x62).start()

def convertValtoVolt(x):
	return int((x/3.3) * 4096.0)


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

		frame = tk.Frame(self)
		frame.pack(side = tk.RIGHT, fill = tk.BOTH)

		chan1 = ttk.Button(frame, text = "Channel 0", command= lambda: self.add(0))
		chan1.pack(pady = 20, padx = 20)
		chan2 = ttk.Button(frame, text = "Channel 1", command=  lambda: self.add(1))
		chan2.pack(pady = 20, padx = 20)
		chan3 = ttk.Button(frame, text = "Channel 2", command=  lambda: self.add(2))
		chan3.pack(pady = 20, padx = 20)
		chan4 = ttk.Button(frame, text = "Channel 3", command=  lambda: self.add(3))
		chan4.pack(pady = 20, padx = 20 )

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

		self.values = [0.05 for x in range(100)]

		self.phaser = 0
		self.gainer = 0.316

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

	def SinwaveformGenerator(self):
	  self.values.append(adc.getADCVAL(self.channel))
	  #self.values.append(np.random.rand()*2 -1)
	  self.after(ms = 25, func= self.SinwaveformGenerator)
	  #time.sleep(0.025)
	  #self.SinwaveformGenerator()

	def RealtimePlotter(self):
	  CurrentXAxis=plt.arange(len(self.values)-100,len(self.values),1)
	  self.line1[0].set_data(CurrentXAxis,plt.array(self.values[-100:]))
	  self.ax.axis([CurrentXAxis.min(),CurrentXAxis.max(), min(self.values[-100:]), max(self.values[-100:])])
	  self.canvas.draw()
	  self.after(ms = 25 , func= self.RealtimePlotter)

if __name__ == "__main__":
	print('Press Ctrl-C to quit...')
	gain = -10
	MAX_GAIN = -10

	keyvals= [10,10]

	xvals = []
	yvals = []

	time.sleep(1)

	x = 0

	while(x <=360):
		a = gain/20
		b = MAX_GAIN/20

		G = 10**a
		Gmax = 10**b
		
		vi = 1.5 + 1.0 * (G/Gmax) * np.cos(x * np.pi/180)
		vq = 1.5 + 1.0 * (G/Gmax) * np.sin(x * np.pi/180)
		
		dac1.updateVal(convertValtoVolt(vi))
		dac2.updateVal(convertValtoVolt(vq))

		time.sleep(0.08)

		val = adc.getADCVAL(0)
		if(abs(val)  < abs(keyvals[1])):
			keyvals[0] = x
			keyvals[1] = val
			
		print("at phase: %s"%(x))
		print('output: %s' % (abs(val)))

		xvals.append(x)
		yvals.append(val)
		x+=0.5


	print('Min Phase: %s' % (keyvals[0]))
	print('Min Voltage: %s' %(keyvals[1]))

	plt.plot(xvals,yvals)
	plt.plot(keyvals[0], keyvals[1], marker='x', color = 'r')
	plt.title('Voltage vs Phase')
	plt.xlabel('Phase (degrees)')
	plt.ylabel('Voltage (V)')

	plt.show()

	print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
	
	phase = keyvals[0]
	keygainvals = [[0, 0, 0], 10]

	xvals2 = []
	yvals2 = []

	while gain >= -40:
		a = gain/20
		b = MAX_GAIN/20

		G = 10**a
		Gmax = 10**b
		vi = 1.5 + 1.0 * (G/Gmax) * np.cos(phase * np.pi/180)
		vq = 1.5 + 1.0 * (G/Gmax) * np.sin(phase * np.pi/180)
		
		biti = convertValtoVolt(vi)
		bitq = convertValtoVolt(vq)
		
		dac1.updateVal(biti)
		dac2.updateVal(bitq)

		time.sleep(0.1)

		val = adc.getADCVAL(0)
		if (abs(val) < abs(keygainvals[1])):
			keygainvals[0][0] = biti
			keygainvals[0][1] = bitq
			keygainvals[0][2] = gain
			keygainvals[1] = val

		print("At gain: %s" % (gain))
		print('output: %s' % (val))

		xvals2.append(gain)
		yvals2.append(val)

		gain -=0.2


	print('Min GAIN: %s' % (keygainvals[0][2]))
	print('Min Voltage: %s' % (keygainvals[1]))

	plt.plot(xvals2, yvals2)
	plt.plot(keygainvals[0][2], keygainvals[1], marker='x', color='r')
	plt.title('Voltage vs Amplitude')
	plt.xlabel('Amplitude (dB)')
	plt.ylabel('Voltage (V)')

	plt.show()

	biti = keygainvals[0][0]
	bitq = keygainvals[0][1]

	print('I bit: %s' % (biti))
	print('Q bit: %s' % (bitq))
	
	dac1.updateVal(biti)
	dac2.updateVal(bitq)
	
	app = MainGui()
	app.mainloop()


	dac1.stop()
	dac2.stop()
	adc.stop()

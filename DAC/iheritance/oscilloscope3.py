import matplotlib.pylab as pylab
import numpy as np
from ADS import ADCThread

xAchse=pylab.arange(0,100,1)
yAchse=pylab.array([0]*100)

fig = pylab.figure(1)
ax = fig.add_subplot(111)
ax.grid(True)
ax.set_title("Realtime Waveform Plot")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.axis([0,100,-5,5])
line1=ax.plot(xAchse,yAchse,'-')

manager = pylab.get_current_fig_manager()

values=[]
values = [0 for x in range(100)]

Ta=0.01
fa=1.0/Ta
fcos=3.5

Konstant=np.cos(2*np.pi*fcos*Ta)
T0=1.0
T1=Konstant

def SinwaveformGenerator(arg):
  global values
  #ohmegaCos=arccos(T1)/Ta
  #print "fcos=", ohmegaCos/(2*pi), "Hz"

  values.append(np.random.rand())

def RealtimePloter(arg):
  global values
  CurrentXAxis=pylab.arange(len(values)-100,len(values),1)
  line1[0].set_data(CurrentXAxis,pylab.array(values[-100:]))
  ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-1.5,1.5])
  manager.canvas.draw()
  #manager.show()

timer = fig.canvas.new_timer(interval=20)
timer.add_callback(RealtimePloter, ())
timer2 = fig.canvas.new_timer(interval=20)
timer2.add_callback(SinwaveformGenerator, ())
timer.start()
timer2.start()

pylab.show()

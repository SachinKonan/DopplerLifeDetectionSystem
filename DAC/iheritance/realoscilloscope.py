import matplotlib.pylab as plt
import numpy as np
from matplotlib import style

style.use("ggplot")

xAchse=plt.arange(0,100,1)
yAchse=plt.array([0]*100)

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.grid(True)
ax.set_title("Realtime Waveform Plot")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.axis([0,100,-5,5])
line1=ax.plot(xAchse,yAchse,'-')

manager = plt.get_current_fig_manager()

values = [0 for x in range(100)]

def SinwaveformGenerator(arg):
  global values
  #ohmegaCos=arccos(T1)/Ta
  #print "fcos=", ohmegaCos/(2*pi), "Hz"

  """Tnext=((Konstant*T1)*2)-T0

  if len(values)%100>70:
    values.append(np.random.rand()*2-1)
  else:
    values.append(Tnext)
  T0=T1
  T1=Tnext"""
  #add adc stuff here
  values.append(np.random.rand()*2 -1)

def RealtimePloter(arg):
  global values
  CurrentXAxis=plt.arange(len(values)-100,len(values),1)
  line1[0].set_data(CurrentXAxis,plt.array(values[-100:]))
  ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-5,5])
  manager.canvas.draw()
  #manager.show()

timer = fig.canvas.new_timer(interval=20)
timer.add_callback(RealtimePloter, ())
timer2 = fig.canvas.new_timer(interval=20)
timer2.add_callback(SinwaveformGenerator, ())
timer.start()
timer2.start()

plt.show()

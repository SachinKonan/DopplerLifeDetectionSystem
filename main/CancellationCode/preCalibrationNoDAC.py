import time
import numpy as np
import matplotlib.pyplot as plt
import random

def convertValtoVolt(x):
	return int((x/3.3) * 4096.0)


if __name__ == "__main__":
	#/home/pi/Documents/PythonProjects/ScienceFair2016/DAC/simptest.py

	time.sleep(1)
	print('Press Ctrl-C to quit...')
	dut = True
	#gain = 0.316
	#dac1.updateVal(convertValtoVolt(2.5))
	#dac2.updateVal(convertValtoVolt(2.5))

	gain = 0.316


	keyvals= [10,10]

	xvals = []
	yvals = []

	time.sleep(1)

	for x in range(0, 361):
		a = gain/20
		b = 0.316/20

		G = 10**a
		Gmax = 10**b
		vi = 1.5 + 1.0 * (G/Gmax) * np.cos(x * np.pi/180)
		vq = 1.5 + 1.0 * (G/Gmax) * np.sin(x * np.pi/180)
		#print("At phase: " + str(x))
		#print("At amp; " + str(gain))

		#print("Voltage I " + str(round(vi,4)))
		#print("Voltage Q " + str(round(vq,4)))
		#dac1.updateVal(convertValtoVolt(vi))
		#dac2.updateVal(convertValtoVolt(vq))

		#time.sleep(0.1)

		val = np.random.rand() * 5
		if(val  < keyvals[1]):
			keyvals[0] = x
			keyvals[1] = val
		print("at phase: %s"%(x))
		print('output: %s' % (val))

		xvals.append(x)
		yvals.append(val)


	print('Min Phase: %s' % (keyvals[0]))
	print('Min Voltage: %s' %(keyvals[1]))

	plt.plot(xvals,yvals)
	plt.plot(keyvals[0], keyvals[1], marker='x', color = 'r',markersize=10)
	plt.title('Voltage vs Phase')
	plt.xlabel('Phase (degrees)')
	plt.ylabel('Voltage (V)')

	plt.show()

	"""
	for x in range(0, 361, 10):
		a = gain/20
		b = 0.316/20

		G = 10**a
		Gmax = 10**b
		vi = 1.5 + 1.0 * (G/Gmax) * np.cos(x * np.pi/180)
		vq = 1.5 + 1.0 * (G/Gmax) * np.sin(x * np.pi/180)
		print("At phase: " + str(x))
		print("At amp; " + str(gain))

		print("Voltage I " + str(round(vi,4)))
		print("Voltage Q " + str(round(vq,4)))
		dac1.updateVal(convertValtoVolt(vi))
		dac2.updateVal(convertValtoVolt(vq))

		time.sleep(1)

	phase = 45
	gain = 0


	while(gain <= 1):
		a = gain/20
		b = 0.316/20

		G = gain
		Gmax = 1
		vi = 1.5 + 1.0 * (G/Gmax) * np.cos(phase * np.pi/180)
		vq = 1.5 + 1.0 * (G/Gmax) * np.sin(phase * np.pi/180)
		print("At phase: " + str(phase))
		print("At amp; " + str(gain))

		print("Vi " + str(round(vi,4)))
		print("Vq " + str(round(vq,4)))
		dac1.updateVal(convertValtoVolt(vi))
		dac2.updateVal(convertValtoVolt(vq))

		gain += 0.05
		time.sleep(1)



	dac1.stop()
	dac2.stop()
	"""

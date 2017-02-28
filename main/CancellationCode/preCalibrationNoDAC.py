import time
import numpy as np
import matplotlib.pyplot as plt

def convertValtoVolt(x):
	return int((x/3.3) * 4096.0)


if __name__ == "__main__":
	#/home/pi/Documents/PythonProjects/ScienceFair2016/DAC/simptest.py

	#adc = ADCThread(address=0x48).start()
	#dac1 = dacThreadVAL(0x63).start()
	#dac2 = dacThreadVAL(0x62).start()

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

	"""
	plt.plot(xvals,yvals)
	plt.plot(keyvals[0], keyvals[1], marker='x', color = 'r')
	plt.title('Voltage vs Phase')
	plt.xlabel('Phase (degrees)')
	plt.ylabel('Voltage (V)')

	plt.show()
	"""

	print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
	MAX_GAIN = -10
	MIN_GAIN = -70
	gain = -10
	phase = keyvals[1]
	keygainvals = [10,10]

	xvals2 = []
	yvals2 = []

	while gain >= -40:
		a = gain/20
		b = MAX_GAIN/20

		G = 10**a
		Gmax = 10**b
		vi = 1.5 + 1.0 * (G/Gmax) * np.cos(phase * np.pi/180)
		vq = 1.5 + 1.0 * (G/Gmax) * np.sin(phase * np.pi/180)

		#print("At gain: %s" % (gain))

		#print("Voltage I " + str(round(vi,4)))
		#print("Voltage Q " + str(round(vq,4)))
		#dac1.updateVal(convertValtoVolt(vi))
		#dac2.updateVal(convertValtoVolt(vq))

		val = np.random.rand()*5

		if(val  < keygainvals[1]):
			keygainvals[0] = gain
			keygainvals[1] = val

		print('At amp: %s'%(gain))
		print('I Bit Equivalent: %s' %(vi))
		print('Q Bit Equivalent: %s'% (vq))
		print('XXXXXXXXXXXXXX')

		xvals2.append(gain)
		yvals2.append(val)

		gain -= 0.2


	print('Min GAIN: %s' % (keygainvals[0]))
	print('Min Voltage: %s' %(keygainvals[1]))

	plt.plot(xvals2,yvals2)
	plt.plot(keygainvals[0], keygainvals[1], marker='x', color = 'r')
	plt.title('Voltage vs Amplitude')
	plt.xlabel('Amplitude (dB)')
	plt.ylabel('Voltage (V)')

	plt.show()

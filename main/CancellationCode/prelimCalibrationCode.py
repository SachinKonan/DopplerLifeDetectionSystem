import time
import numpy as np
from setvalue import dacThreadVAL
from ADS import ADCThread
import matplotlib.pyplot as plt

def convertValtoVolt(x):
	return int((x/3.3) * 4096.0)

if __name__ == "__main__":
	#/home/pi/Documents/PythonProjects/ScienceFair2016/DAC/simptest.py

	adc = ADCThread(address=0x48).start()
	dac1 = dacThreadVAL(0x63).start()
	dac2 = dacThreadVAL(0x62).start()

	time.sleep(1)
	print('Press Ctrl-C to quit...')
	dut = True
	#gain = 0.316
	#dac1.updateVal(convertValtoVolt(2.5))
	#dac2.updateVal(convertValtoVolt(2.5))

	gain = -10
	GMAX = -10
	
	keyvals= [10,10]

	xvals = []
	yvals = []

	time.sleep(1)

	x = 0

	while(x <=360):
		a = gain/20
		b = GMAX/20
		
		G = 10**a
		Gmax = 10**b
		vi = 1.5 + 1.0 * (G/Gmax) * np.cos(x * np.pi/180)
		vq = 1.5 + 1.0 * (G/Gmax) * np.sin(x * np.pi/180)
		#print("At phase: " + str(x))
		#print("At amp; " + str(gain))

		#print("Voltage I " + str(round(vi,4)))
		#print("Voltage Q " + str(round(vq,4)))
		dac1.updateVal(convertValtoVolt(vi))
		dac2.updateVal(convertValtoVolt(vq))

		time.sleep(0.1)

		val = adc.getADCVAL(0)
		if(val  < keyvals[1]):
			keyvals[0] = x
			keyvals[1] = val
		print("at phase: %s"%(x))
		print('output: %s' % (val))

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
	MAX_GAIN = -10
	MIN_GAIN = -60
	gain = -10
	phase = keyvals[0]
	keygainvals = [10,10]

	xvals2 = []
	yvals2 = []

	while gain >= -50:
		a = gain/20
		b = MAX_GAIN/20

		G = 10**a
		Gmax = 10**b
		vi = 1.5 + 1.0 * (G/Gmax) * np.cos(phase * np.pi/180)
		vq = 1.5 + 1.0 * (G/Gmax) * np.sin(phase * np.pi/180)
		
		dac1.updateVal(convertValtoVolt(vi))
		dac2.updateVal(convertValtoVolt(vq))

		time.sleep(0.1)
		
		val = adc.getADCVAL(0)
		if(val  < keygainvals[1]):
			keygainvals[0] = gain
			keygainvals[1] = val
			
		print("At gain: %s" % (gain))
		print('output: %s' % (val))
		
		xvals2.append(gain)
		yvals2.append(val)

		gain -=1


	print('Min GAIN: %s' % (keygainvals[0]))
	print('Min Voltage: %s' %(keygainvals[1]))

	plt.plot(xvals2,yvals2)
	plt.plot(keygainvals[0], keygainvals[1], marker='x', color = 'r')
	plt.title('Voltage vs Amplitude')
	plt.xlabel('Amplitude (dB)')
	plt.ylabel('Voltage (V)')

	plt.show()
	
	
	dac1.stop()
	dac2.stop()
	adc.stop()
	
	
	"""
	xlist = []
	ylist = []
	
	for x in range(0, 200,1):
		xlist.append(x)
		ylist.append(adc.getADCVAL(0))
		time.sleep(0.1)
		
	plt.plot(xlist,ylist)
	
	plt.title('Control')
	plt.xlabel('Samples')
	plt.ylabel('Voltage (V)')
	plt.show()
	
	print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

	MAX_GAIN = 0.316

	phase = keyvals[0]
	keygainvals = [10,10]

	xvals2 = []
	yvals2 = []

	i = 0
	while i <= 1 :
		vi = 1.5 + 1.0 * (i) * np.cos(phase * np.pi/180)
		vq = 1.5 + 1.0 * (i) * np.sin(phase * np.pi/180)

		print("At gain: %s" % (i))
	
	MAX_GAIN = 0.316

		print("Voltage I: %s" % (round(vi,4)))
		print("Voltage Q: %s" % (round(vq,4)))
		dac1.updateVal(convertValtoVolt(vi))
		dac2.updateVal(convertValtoVolt(vq))

		time.sleep(0.1)

		val = adc.getADCVAL(0)
		if(val  < keygainvals[1]):
			keygainvals[0] = i
			keygainvals[1] = val

		#print('At amp: %s'%(gain))
		#print('I Bit Equivalent: %s' %(int((vi/3.3) * 4096)))
		#print('Q Bit Equivalent: %s'% (int((vq/3.3) * 4096)))
		#print('XXXXXXXXXXXXXX')

		xvals2.append(i)
		yvals2.append(val)

		i += 0.001


	print('Min GAIN: %s' % (keygainvals[0]))
	print('Min Voltage: %s' %(keygainvals[1]))

	plt.plot(xvals2,yvals2)
	plt.plot(keygainvals[0], keygainvals[1], marker='x', color = 'r')
	plt.title('Voltage vs Amplitude')
	plt.xlabel('Amplitude (dB)')
	plt.ylabel('Voltage (V)')

	plt.show()
	
	"""

	"""
	print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
	MAX_GAIN = 0.316
	MIN_GAIN = -40
	gain = 0.316
	phase = keyvals[0]
	keygainvals = [10,10]

	xvals2 = []
	yvals2 = []

	while gain >= -50:
		a = gain/20
		b = MAX_GAIN/20

		G = 10**a
		Gmax = 10**b
		vi = 1.5 + 1.0 * (G/Gmax) * np.cos(phase * np.pi/180)
		vq = 1.5 + 1.0 * (G/Gmax) * np.sin(phase * np.pi/180)
		
		dac1.updateVal(convertValtoVolt(vi))
		dac2.updateVal(convertValtoVolt(vq))

		time.sleep(0.1)
		
		val = adc.getADCVAL(0)
		if(val  < keygainvals[1]):
			keygainvals[0] = gain
			keygainvals[1] = val
			
		print("At gain: %s" % (gain))
		print('output: %s' % (val))
		
		xvals2.append(gain)
		yvals2.append(val)

		gain -=1


	print('Min GAIN: %s' % (keygainvals[0]))
	print('Min Voltage: %s' %(keygainvals[1]))

	plt.plot(xvals2,yvals2)
	plt.plot(keygainvals[0], keygainvals[1], marker='x', color = 'r')
	plt.title('Voltage vs Amplitude')
	plt.xlabel('Amplitude (dB)')
	plt.ylabel('Voltage (V)')

	plt.show()
	
	
	
	print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
	MAX_GAIN = 0.316
	MIN_GAIN = -40
	gain = 0.316
	phase = keyvals[1]
	keygainvals = [10,10]

		print("Voltage I: %s" % (round(vi,4)))
		print("Voltage Q: %s" % (round(vq,4)))
		dac1.updateVal(convertValtoVolt(vi))
		dac2.updateVal(convertValtoVolt(vq))

		time.sleep(0.1)

		val = adc.getADCVAL(0)
		if(val  < keygainvals[1]):
			keygainvals[0] = gain
			keygainvals[1] = val

		#print('At amp: %s'%(gain))
		#print('I Bit Equivalent: %s' %(int((vi/3.3) * 4096)))
		#print('Q Bit Equivalent: %s'% (int((vq/3.3) * 4096)))
		#print('XXXXXXXXXXXXXX')

		xvals2.append(gain)
		yvals2.append(val)

		gain -= 0.2
	
	print('MIN Phase: %s' %(phase))
	print('Min GAIN: %s' % (keygainvals[0]))
	print('Min Voltage: %s' %(keygainvals[1]))

	plt.plot(xvals2,yvals2)
	plt.plot(keygainvals[0], keygainvals[1], marker='x', color = 'r')
	plt.title('Voltage vs Amplitude')
	plt.xlabel('Amplitude (dB)')
	plt.ylabel('Voltage (V)')
	
	
	plt.show()
	
	"""
	
	

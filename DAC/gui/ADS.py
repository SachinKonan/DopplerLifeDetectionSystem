import time
import Adafruit_ADS1x15
from threading import Thread

class ADCThread:
	def __init__(self,address = 0x48,gain=2/3,numthreads =1):
		self.i2caddress = address
		self.adc = Adafruit_ADS1x15.ADS1115(self.i2caddress)
		self.GAIN = gain
		self.numthreads = numthreads
		self.interrupt = False
		self.stopA1 = False
		self.stopA2 = False
		self.stopA3 = False
		self.adcval1 = 0
		self.adcval2 = 0
		self.adcval3 = 0
		self.adcval4 = 0
		self.samples = 0
		self.start_time = 0
		self.end_time = 0
		self.samplingrate = 0

	def start(self):
		Thread(target= self.channel,args =()).start()
		return self
		#self.start_time = time.time()
		#Thread(target = self.channel2,args = ()).start()

	def channel(self):
		i = 0
		i1 = 1
		while True:

			if(self.interrupt):
				return

			else:
				self.adcval1 = (self.adc.read_adc(0, gain=self.GAIN)/32767.0)* 6.144
				self.adcval2 = (self.adc.read_adc(1, gain=self.GAIN)/32767.0)* 6.144
				self.adcval3 = (self.adc.read_adc(2, gain=self.GAIN)/32767.0)* 6.144
				self.adcval4 = (self.adc.read_adc(3, gain=self.GAIN)/32767.0)* 6.144
				#self.end_time = time.time()
				#self.samples+=1
				time.sleep(0.01)
	def getADCVal1(self):
		return self.adcval1

	def getADCVal2(self):
		return self.adcval2

	def getADCVal3(self):
		return self.adcval3

	def getADCVal4(self):
		return self.adcval4

	"""
	def calcSamplingRate(self):
		tottime = self.end_time - self.start_time
		return self.samples/tottime

	def printnumSamples(self):
		return self.samples
	"""

	def stop(self):
		self.interrupt = True

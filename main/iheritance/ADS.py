import time
import Adafruit_ADS1x15
from threading import Thread


dic = {
2/3: 6.144,
1: 4.096,
2: 2.048,
4: 1.024,
8: 0.512.
16, 0.256
}

class ADCThread:
	def __init__(self,address,gain= 2/3,numthreads =1):
		self.i2caddress = address
		self.GAIN = gain
		self.adc = Adafruit_ADS1x15.ADS1115(address,gain=)
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
		self.voltVal = dic[gain]
		
	def start(self):
		Thread(target= self.channel1,args =()).start()
		return self
		#self.start_time = time.time()
		#Thread(target = self.channel2,args = ()).start()
	
	def channel1(self):
		i = 0
		i1 = 1
		while True:
			
			if(self.interrupt):
				
				return
			
			else:
				self.adcval1 = self.adc.read_adc(0, gain=self.GAIN)
				self.adcval2 = self.adc.read_adc(1, gain=self.GAIN)
				self.adcval3 = self.adc.read_adc(2, gain=self.GAIN)
				self.adcval4 = self.adc.read_adc(3, gain=self.GAIN)
				#self.end_time = time.time()
				#self.samples+=1
				time.sleep(0.01)
				
	def getADCVal1(self):
		return (self.adcval1/32767.0) * 6.144
	
	def getADCVal2(self):
		return self.adcval2
	
	def getADCVal3(self):
		return self.adcval3
	
	def getADCVal4(self):
		return self.adcval4
	
	
	def convertValtoVolt(x):
		return (x/32767.0) * 6.144
		
	"""
	def calcSamplingRate(self):
		tottime = self.end_time - self.start_time
		return self.samples/tottime
	
	def printnumSamples(self):
		return self.samples		
	"""
		
	def stop(self):
		self.interrupt = True


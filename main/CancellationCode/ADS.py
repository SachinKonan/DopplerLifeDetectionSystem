import time
import Adafruit_ADS1x15
from threading import Thread

dictionary = {
2/3: 6.144,
1: 4.0
}
class ADCThread:
	def __init__(self,address = 0x48,gain=2/3,diff = False):
		self.i2caddress = address
		self.adc = Adafruit_ADS1x15.ADS1115(self.i2caddress)
		self.GAIN = gain
		self.diff = False
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
				if(!self.diff):
					self.adcval1 = (self.adc.read_adc(0, gain=self.GAIN) )
					self.adcval2 = (self.adc.read_adc(1, gain=self.GAIN)/32767.0)* 6.144
					self.adcval3 = (self.adc.read_adc(2, gain=self.GAIN)/32767.0)* 6.144
					self.adcval4 = (self.adc.read_adc(3, gain=self.GAIN)/32767.0)* 6.144
					#self.end_time = time.time()
					#self.samples+=1
				else:
					#  - 0 = Channel 0 minus channel 1
				    #  - 1 = Channel 0 minus channel 3
				    #  - 2 = Channel 1 minus channel 3
				    #  - 3 = Channel 2 minus channel 3
					self.adcval1 = (self.adc.read_adc_difference(0, gain=GAIN))
				time.sleep(0.0005)

	def getADCVAL(self, var):
		if(var == 0): return self.adcval1
		elif(var == 1): return self.adcval2
		elif(var == 2): return self.adcval3
		elif(var == 3): return self.adcval4
		else: pass


	def stop(self):
		self.interrupt = True

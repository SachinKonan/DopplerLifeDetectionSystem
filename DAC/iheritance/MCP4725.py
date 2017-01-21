import time
import numpy as np
from threading import Thread
import Adafruit_MCP4725


class MCP4725:
    def __init__(self, address):
        self.i2caddress = address
        self.interrupt = False
        self.dac = Adafruit_MCP4725.MCP4725(self.i2caddress)

    def start(self):
        Thread(args=(),target=self.cycle)

    def cycle(self):
        if(self.interrupt):
            return
        else:
            pass

    def stop(self):
        self.interrupt = True

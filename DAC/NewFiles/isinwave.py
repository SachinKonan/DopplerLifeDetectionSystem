import time

import numpy as np

from DAC.NewFiles.MCP4725 import MCP4725


class dacThreadSin(MCP4725):
    def __init__(self,address,frequency = 1):
        super.__init__(address=address)
        self.degree = 0
        self.frequency = frequency

    def cycle(self):
        while True:

            if (self.interrupt):
                return

            else:
                radians = (self.degree * np.pi / 180)
                val = np.sin(2 * np.pi * self.frequency * np.radians(self.degree)) * 2048 + 2048
                # print(val)
                self.dac.set_voltage(int(round(val)), True)
                self.checkdegree()
                time.sleep(0.1)

    def checkdegree(self):
        """
        if(self.degree > 360):
            self.degree = 0
        else:
            self.degree = self.degree
            """
        self.degree += 1

    def stop(self):
        self.interrupt = True
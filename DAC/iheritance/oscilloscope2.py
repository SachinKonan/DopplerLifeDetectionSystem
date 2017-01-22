import serial
import matplotlib.pyplot as plt
from drawnow import *
import atexit
from ADS import ADCThread


def plotValues():
    plt.title('Serial value from Arduino')
    plt.grid(True)
    plt.ylabel('Values')
    plt.plot(values, 'rx-', label='values')

    plt.legend(loc='upper right')

def doAtExit():
    adc.stop()
    print("ADS115 is " + adc.interrupt)
values = []

plt.ion()
cnt=0

adc = ADCThread(0x48)

atexit.register(doAtExit)

print("ADS is open: " )

#pre-load dummy data
for i in range(0,26):
    values.append(0)

while True:
    valueRead = adc.getADCVal1()

    #check if valid value can be casted
    try:
        valueInInt = int(valueRead)
        print(valueInInt)
        if valueInInt >= 0:
            values.append(valueInInt)
            values.pop(0)
            drawnow(plotValues)
            else:
                print("Invalid! negative number")
    except ValueError:
        print("Invalid! cannot cast")

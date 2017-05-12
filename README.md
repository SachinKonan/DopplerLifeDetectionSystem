# Doppler Radar Based Life Detection System

This project aimed at designing a low-cost Doppler radar system capable of detectin earthquake victims buried under rubble. The original system started with a cheap HB-100 system (located in ScienceFair2016), but after a summer's worth of research a from-scratch system was redesigned, requiring electrical and software innovation. The radar features a front-end clutter cancellation system which enables it to ignore the strong frontal reflections, allowing it to have hypersensitivity to signals through the rubble. Current work lies with redesigning the system on a printed circuit board for mobile deployment. 
![alt text](https://github.com/SachinKonan/DopplerLifeDetectionSystem/blob/master/RadarFull/fullphysicalradar.jpg "Doppler")

## Research Paper
The full, Latex Paper can be found under the Research tab. 

## Hardware Build

The Schematic for the entire radar is found under the RadarFull tab. This includes the connections of the RF components, the filter/amplifier circuit, power supply, and list of materials.

### PCB

A PCB radar was designed on Upverter and the gerber files can be found in the PCBRadar folder. 

## Software

### Simple Oscillscope

Under main/SimpleOscilloscope a oscilloscope was designed as an intermediate step in the project, but may be a useful tool for anyone looking to debug circuits. The oscilloscope has a simple gui interface and the hookups of the connections can be found on the start page of the gui. 

### DAC And ADC Support

In order to speed up ADC and DAC control, threaded classes for the ADS-1115 and MCP-4725 were constructed -- main/ADC and main/DAC. These classes require the bare-bone libraries provided by adafruit: 

https://github.com/adafruit/Adafruit_Python_ADS1x15

https://github.com/adafruit/Adafruit_Python_MCP4725

These classes will run idly while simple getters and setters can be used to manipulate inputs/outputs. Additionally within the DAC folder sample classes for sin-wave, triangle-wave, square wave, and user set wave are provided. 

### Signal Processing

A FIR Filter and a Custom Signal Processing algorithm can be found in main/DSP. The Signal Processing algorithm is described in the paper. 

### Clutter Cancellatiion 

Found under main/Clutter-Cancellation. Currently in rats-nest state as the majority of testing occured in this folder. The results of the testing in the filter are found in the realmain.py file in main

### Radar Simulations

To demonstrate that DC offset corresponds to the amount of clutter in the radar system, a python simulation was constructed which can be found in main/Simulations. Once run
### Final

Once all pin connections are made correct according to the picture in main/radarfull.png, main/realmain.py can be run, which has three tabs.

1) Clutter Cancellation - Will run cancellation algorithm and minimize clutter in the receive antenna (approach described in paper). 
2) Data Collection and Processing - Will collect 2500 samples and output an FFT of the processed data. 
3) Simple Oscilloscope - Can be used for debugging within the system. 

# Author
Sachin Konan - Have been working on this work for 1.5 years +
James Aberle - Mentor for the project, aiding in rf clutter cancellation design. 

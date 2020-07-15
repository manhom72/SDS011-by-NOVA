# SDS011-by-NOVA
Reads data from SDS011 air quality sensor and shows an AQI (Air Quality Index)

## TABLE OF CONTENTS
* [Geeneral Info] - What does this code
* [Included Files] - Files included in the project
* [Techologies] - What techonologies have been used or are involved
* [Setup] - Some simple setup advice
* [Future updates] - New features and improvements for future versions

## General Info
Project created by Manuel Hompanera, July 2020.

This code reads the data from the SDS011 air quality sensor using UART protocol and transforms the binary data to the US - Environmenta Protection Agengy air quality (AQI) values.

## Included files
At the time of this update, July 2020 14th, this project has only two files:
  - SDS011_2_0.py: reads the data using UART protocol and gives values of US - EPA air quality index.
  - README file.

## Technologies
* The project is created with Python 3,7 version
* CH340 chip based USB adaptor. CH340 drivers might be installed before running the program. Make sure you install an updated version of the drivers.

## Setup
To install the program, you just need to copy or download the SDS011_2_0.py file to a computer that runs a 3.7 version of Python or higher.

In the Python script you have to change two things before running the program:

* 1.- USB port of your computer.
It depends on the OS. The values for Windows systems can be COM3, COM4,...
In macOS it is usually something like /dev/tty.usbserial1410 or /dev/tty.usbserial1420, ...
You have to check your system.

* 2.- File name for readings
You may whant to change the name of the file where the AQI values are written.
By default this is "sds011.txt"

* 3.- The number of readings
It is set by default for 3 readings. Depending on the working mode of the sensor, each reading can be fast or take a while.

## Future updates
One cool feature of the SDS011 is that you can change the working mode. This means that you can make readings in continuous mode, wich is default, or in intervals of 1-30minute:(work 30 seconds and sleep n*60-30 seconds).
In a new update I will upload more scripts to change the working mode of the sensor and to start and stop.


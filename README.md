# SDS011-by-NOVA
Reads data from SDS011 air quality sensor and shows an AQI (Air Quality Index)
Project created by Manuel Hompanera, July 2020.

I am almost new to GitHub and not very expecienced yet in programming, and I use this files to practice and learn. If you have any suggestion, please feel free to share ccp.mhr@gmail.com.

## TABLE OF CONTENTS
* [General Info] - What does this program?
* [Main Features] - What features are included?
* [Included Files] - Files included in the project
* [Techologies] - What techonologies have been used or are involved
* [Setup] - Some simple setup advice
* [Future updates] - New features and improvements for future versions

## General Info
This code reads the data from the SDS011 air quality sensor by Nova using UART protocol and transforms the binary data to the US - Environmenta Protection Agengy air quality (AQI) values. Those values range from "Good" to "Hazarduous". More information on the index can be found here: https://cfpub.epa.gov/airnow/index.cfm?action=aqibasics.aqi

The device by default will make readings in continuous working mode. According to de datasheet the expected life for the device is arount 8000 hrs. It is not sure than reducing the frequency of the readings will expand life. But I've tried, and this can be done from 0 (continuous) to 30 minutes. The device will make readings for 30 seconds, then sleep for (n * 60 - 30 seconds), where n is the number of minutes.

## Main Features
With this program you can:
* Calculate the Air Quality Index. Values for particulate matter are also given in micrograms/m3.
* Display the device main parameters, like the working mode, the working period, the device ID number and the firmware version
* Change the device working period. Values can range from 0 to 30 minues.
* Change the working mode -- NOTE: even if the menu offers this option, it cannot yet be done. It will be realeased in a future version of the program.

## Included files
At the time of this update, July 2020 16th, this project has only three files:
  - SDS011_2_0.py: this is the main program, it reads the data using UART protocol and gives values of US - EPA air quality index.
  - deviceC.py: includes classes used by the main program
  - README file.

## Technologies
* The project is created with Python 3,7 version
* CH340 chip based USB adaptor. CH340 drivers might be installed before running the program. Make sure you install an updated version of the drivers.
* You also need pySerial. You can find information here: https://pythonhosted.org/pyserial/

## Setup
To install the program, you just need to copy or download the files to a computer that runs a 3.7 version of Python or higher.

In the Python script you should change two things before running the program:

* 1.- USB port of your computer - Mandatory -.
It depends on the OS. The values for Windows systems can be COM3, COM4,...
In macOS it is usually something like /dev/tty.usbserial1410 or /dev/tty.usbserial1420, ...
You have to check your system.

* 2.- File name for readings - Optional -.
You may whant to change the name of the file where the AQI values are written.
By default this is "sds011.txt"

* 3.- The number of readings - Optional -.
It is set by default for 3 readings. Depending on the working mode of the sensor, each reading can be fast or take a while. Unless you want the sensor to be working for a very longtime, I'd use low numbers

## Future updates
In future updates I would create a framework with Flask and Jinja2, so the interaction with the program by the user can be done with a browser.


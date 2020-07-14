# OPENS THE SERIAL, RECEIVES DATA AND PRINTS IT ON THE SCREEN
# ADDITIONALY, IT SAVES THE READINGS TO A FILE CALLED file_name
# BEFORE IT STARTS READING, THE PROGRAM ASKS FOR A LOCATION NAME
# THIS CAN BE WATHEVER STRING YOU'D LIKE, IT'S ONLY TO WRITE
# INFORMATION IN THE FILE.
import serial
from datetime import datetime

# SET UP VARIABLES
# this is the name of the port where the CH340 is connected
# this must be changed according to your needs and OS
# see README file for more info
usbport = '/dev/tty.wchusbserial1410'

# name of the file to save the readings
file_name = "sds011.txt"

# number of measurements
number_of_measurements = 3

# US - EPA values 
# ranges in the aqi table for calculation
table_values_for_pm25_epa = (0,12, 35.4, 55.4, 150.4, 250.4, 350.4, 500.4)
table_values_for_pm10_epa = (0, 54, 154, 254, 354, 424, 504, 604)
table_values_for_aqi_epa = (0, 50, 100, 150, 200, 300, 400, 500)


ser = serial.Serial(usbport, baudrate=9600, stopbits=1,
                    parity='N', timeout=None, write_timeout=0)


def calculates_aqi(values) -> list:
    """Assumes values a list with pm25 index and pm10 index.
       Returns a list with the AQI EPA index. pm25 first, then pm10."""
    # values[0] gives the pm25 in micrograms/m3
    # values[1] gives teh pm10 in micrograms/m3
    pm_index = [0, 0]
    pm_index[0] = select_from_aqi_table(values[0], table_values_for_pm25_epa, 0.1)
    pm_index[1] = select_from_aqi_table(values[1], table_values_for_pm10_epa, 1.0)
    return pm_index


def select_from_aqi_table(average_value: float, current_aqi_table: tuple, increment: float) -> list:
    """Chooses the right values from the EPA tables.
       Selects the range for the AQI calculation
       Returns the calculated AQI value."""
    pair_of_values = [0,0,0,0]      # [ilow, ihigh, clow, chigh] in aqi table & formula
    i = 0
    while average_value >= current_aqi_table[i]:
            i += 1
    if i <= 1:
        pair_of_values[-2] = 0
        pair_of_values[0] = 0
    else:
        pair_of_values[-2] = current_aqi_table[i-1] + increment
        pair_of_values[0] = table_values_for_aqi_epa[i-1] + 1
    pair_of_values[-1] = current_aqi_table[i]
    pair_of_values[1] = table_values_for_aqi_epa[i]
    # the following formula returns the aqi value:
    aqi_index = (pair_of_values[1] - pair_of_values[0]) * (average_value-pair_of_values[-2]) / (pair_of_values[-1] - pair_of_values[-2]) + pair_of_values[0]
    return aqi_index


# trying to read data and print it on the screen
def read_data_from_sensor() -> list:
    """Waits until data is received from the sensor.
       Returns a list of integers from the sensor."""
    s = ser.read(10)
    print(s)
    read_line = []
    for i in s:
        read_line.append(i)
    print(read_line, type(read_line[0]))
    return read_line


def transforms_data_to_measurement(given_data):
    """Assumes given_data a list of integers received from SDS011.
       Returns a list with the measurements in micrograms/m3."""
    pm25_reading = ((given_data[3] * 256 + given_data[2]) / 10)
    print(given_data[3], given_data[2], pm25_reading)
    pm10_reading = ((given_data[5] * 256 + given_data[4]) / 10)
    measurements = [pm25_reading, pm10_reading]
    print('--> pm2.5: ', pm25_reading,
          'microgr/m3 --- pm10: ', pm10_reading, 'microgr/m3')
    return measurements


def shows_aqi_index(aqi_values):
    """Assumes values a list with pm25 index and pm10 index.
       Prints the results in the screen."""
    print('AQI 2.5 = ', int(aqi_values[0]), '     AQI 10 = ',
          int(aqi_values[1]))


def prints_to_file(location, aqi_index_value):
    """Assumes location a description of the location,
       aqi_index_value a list with date and aqi indexes.
       Appends all to a file."""
    with open(file_name, 'a') as fb:
        print(location, datetime.today(), int(aqi_index_value[0]),
              int(aqi_index_value[1]), file=fb)


# STARTING HERE:
location_name = input('Select a name to identify location:')
for i in range(number_of_measurements):
    sensor_given_data = read_data_from_sensor()
    print(sensor_given_data)
    aqi_measurements = transforms_data_to_measurement(sensor_given_data)
    aqi_index_result = calculates_aqi(aqi_measurements)
    shows_aqi_index(aqi_index_result)
    prints_to_file(location_name, aqi_index_result)


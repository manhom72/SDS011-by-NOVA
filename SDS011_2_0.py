# OPENS THE SERIAL, RECEIVES DATA AND PRINTS IT ON THE SCREEN
# IN ADDITION, IT SAVES THE READINGS TO A FILE CALLED file_name
# BEFORE IT STARTS READING, THE PROGRAM ASKS FOR A LOCATION NAME
# THIS CAN BE WHATEVER STRING YOU'D LIKE, IT'S ONLY TO WRITE
# INFORMATION IN THE FILE.
import serial
import sys
from datetime import datetime
from deviceC import SDS011

# SET UP VARIABLES --- VARIABLES TO CHANGE ---
# this is the name of the port where the CH340 is connected
# this must be changed according to your needs and OS
# see README file for more info
usbport = '/dev/tty.wchusbserial1410'

# name of the file to save the readings
file_name = "sds011.txt"

# number of measurements
number_of_measurements = 3
# ------  END OF VARIABLES TO CHANGE -----

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


def air_quality_index():
    """Starts the AQI calculator module."""
    location_name = input('Select a name to identify location:')
    done_measurements = 0
    for i in range(number_of_measurements):
        done_measurements += 1
        print('Value', done_measurements, 'of', number_of_measurements,'...')
        sensor_given_data = read_data_from_sensor()
        print(sensor_given_data)
        aqi_measurements = transforms_data_to_measurement(sensor_given_data)
        aqi_index_result = calculates_aqi(aqi_measurements)
        shows_aqi_index(aqi_index_result)
        prints_to_file(location_name, aqi_index_result)
    main_menu()


# This must be eventually simplified?
def bytes_format_converter(in_bytes: bytes)->list:
    """Assumes in_bytes to be in bytes format.
    Returns in hexadecimal format."""
    count = 0
    in_hex = []
    values = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    bytes_list = list(in_bytes.hex())
    for i in bytes_list:
        if count in values:
            first = bytes_list[count]
            second = bytes_list[count+1]
            in_hex.append(first + second)
        else:
            pass
        count += 1
    return in_hex


def send_query_to_sensor(query: str) -> list:
    """Assumes query to be a string.
    Returns a list"""
    ser.write(bytearray.fromhex(query))
    s = ser.read(10)
    resp = bytes_format_converter(s)
    return resp


def get_valid_values(value, min_value, max_value):
    """Assumes value a string, min_value and max_value integers.
    If value is in the range returns True.
    Otherwise returns False."""
    valid_values = [i for i in range(min_value, max_value + 1)]
    print('Those are my valid values:', valid_values)
    try:
        value = int(value)
        print(value, type(value))
    except ValueError:
        print(value, type(value))
        return False
    if value in valid_values:
        return True
    return False


def print_menu_items(values):
    """Assumes values to be a set of possible values.
    Prints a list of items in values."""
    for i in values:
        print(i)


def checksum_byte_calculator(hex_values):
    """Assumes hex_values a string with hex values.
    Returns the low 8bit checksum for the data."""
    hex_values = bytearray.fromhex(hex_values)
    addition = 0
    checksum = ''
    for i in range(2,17):
        addition += hex_values[i]
    letters = [i for i in str(hex(addition))]
    for k in range(-2, 0):
        checksum += letters[k]
    return checksum


def ask_for_values(data_dict):
    """Assumes data_dict to be a dictionary.
    Returns an int between an allowed range."""
    # the dictionary contains the following key/values:
    # min_value, max_value, menu_items, menu_question
    condition = False
    while condition is not True:
        print_menu_items(data_dict['menu_items'])
        selection = input(data_dict['menu_question'])
        try:
            condition = get_valid_values(selection, data_dict['min_value'], data_dict['max_value'])
        except ValueError:
            print('***Something went wrong!')
            print('Choose a valid value from', str(data_dict['min_value']), 'to', str(data_dict['max_value']))
        if condition is True:
            selection = int(selection)
    return selection


def change_working_period():
    """Changes the working period.
    Valid values from 0 to 30 minutes."""
    # WE CREATE A DICTIONARY FOR THE MENU
    menu_paramteters = {'min_value': 0, 'max_value': 30,
                        'menu_items': ('-> 0 minutes stands for continuous working mode',
                                       '-> Maximum value is 30 minutes',
                                       '-> It works 30 seconds and sleeps n*60-30 seconds'),
                        'menu_question': 'Choose the new working period between 0 and 30 minutes: '}
    working_minutes = bytearray(ask_for_values(menu_paramteters).to_bytes(1, 'big')).hex()
    # this inserts the new value in minutes
    string_to_change = (device_commands['set_working_period'])
    data_for_checksum = string_to_change[:12] + working_minutes + string_to_change[14:]
    new_checksum = checksum_byte_calculator(data_for_checksum)
    new_working_period = data_for_checksum[:-5] + new_checksum + data_for_checksum[-3:]
    send_query_to_sensor(new_working_period)
    print()
    print('* WORKING PERIOD CHANGED *')
    show_device_parameters()

    
def change_working_mode():
    """Changes the working mode.
    Returns active mode or query mode."""
    print('Not yet operational - sorry!')
    main_menu()


def show_device_parameters():
    """Shows the main parameters of the device"""
    working_mode = device01.query_working_mode()
    working_period = device01.query_working_period(send_query_to_sensor(device_commands['query_work_period']))
    device_firmware = device01.get_firmware(send_query_to_sensor(device_commands['query_firmware']))
    device_status = device01.query_device_status(send_query_to_sensor(device_commands['query_status']))
    print('---- SENSOR PARAMETERS ----')
    print(device01.__str__())
    print('Current mode is', working_mode)
    print('Working period set to', working_period)
    print('Firmware version: ', device_firmware)
    print('The device is currently', device_status)
    print('-' * 20)
    main_menu()


def main_menu():
    """This is the main menu.
    Redirects to specific functions."""
    # WE CREATE A DICTIONARY FOR THE MAIN MENU
    menu_parameters = {'min_value': 1, 'max_value': 4,
                       'menu_items': ('**** MAIN MENU ****', '1 - Read AQI values', '2 - Change working period',
                                       '3 - Change working mode', '4 - Exit'),
                       'menu_question': 'Choose an option between 1 and 4: '}
    choose_action = ask_for_values(menu_parameters)
    print('Your choice:', choose_action)
    if choose_action == 1:
        print('You choose to calculate AQI')
        air_quality_index()
    elif choose_action == 2:
        print('You choose to change working mode')
        change_working_period()
    elif choose_action == 3:
        print('You choose to change working mode')
        change_working_mode()
    elif choose_action == 4:
        print('Exit program!')
        sys.exit()
    else:
        print('Something went wrong. Bye!')
        sys.exit()


# Those are the main commands we are using to send to the device in order to get/send information
device_commands={'query_work_mode':'AA B4 02 00 00 00 00 00 00 00 00 00 00 00 00 FF FF 00 AB',
                 'query_work_period': 'AA B4 08 00 00 00 00 00 00 00 00 00 00 00 00 FF FF 06 AB',
                 'query_firmware': 'AA B4 07 00 00 00 00 00 00 00 00 00 00 00 00 FF FF 05 AB',
                 'query_status': 'AA B4 06 00 00 00 00 00 00 00 00 00 00 00 00 FF FF 04 AB',
                 'set_working_period': 'AA B4 08 01 XX 00 00 00 00 00 00 00 00 00 00 FF FF 00 AB'}
# the XX in the 'set_working_period' is there because this value in the dictionary is going to be changed
# this is the place where you put new value for the working period in minutes (from 0 to 30)

# Query the current device ID, active mode or query mode
curr_mode = send_query_to_sensor(device_commands['query_work_mode'])
# instantiates current device
device01 = SDS011(curr_mode)
show_device_parameters()

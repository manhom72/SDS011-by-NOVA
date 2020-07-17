class SDS011(object):
    """A class SDS011 defines any device and its commands."""
    def __init__(self):
        self.query_work_mode = 'AA B4 02 00 00 00 00 00 00 00 00 00 00 00 00 FF FF 00 AB'
        self.query_work_period = 'AA B4 08 00 00 00 00 00 00 00 00 00 00 00 00 FF FF 06 AB'
        self.query_status = 'AA B4 06 00 00 00 00 00 00 00 00 00 00 00 00 FF FF 04 AB'
        self.query_firmware = 'AA B4 07 00 00 00 00 00 00 00 00 00 00 00 00 FF FF 05 AB'
        self.set_working_status = 'AA B4 08 01 XX 00 00 00 00 00 00 00 00 00 00 FF FF 00 AB'

    def query_work_mode_command(self):
        return self.query_work_mode

    def query_work_period_command(self):
        return self.query_work_period

    def query_status_command(self):
        return self.query_status

    def query_firmware_command(self):
        return self.query_firmware

    def set_working_status_command(self):
        return self.set_working_status

    def __str__(self):
        return 'Object of type SDS011 main commands.'


class SDS011Device(SDS011):
    """A class SDS011Device defines the attributes of a particular
    SDS011 sensor."""
    # attributes of the object (device parameters) initialized
    def __init__(self, name):
        SDS011.__init__(self)
        self.device_id = name
        self.work_mode = ''
        self.work_period = ''
        self.work_status = ''
        self.firmware = ''

    def get_device_id(self):
        return self.device_id

    def get_work_mode(self):
        return self.work_mode

    def get_work_period(self):
        return self.work_period

    def get_work_status(self):
        return self.work_status

    def get_firmware(self):
        return self.firmware

# add methods to the object:
    def set_working_period(self, other):
        """Changes the working period of self."""
        # you write the info through the main program
        # here you only update the instance
        self.work_period = other
        return self.work_period

    def set_working_mode(self, other):
        """Changes the working mode of self"""
        self.work_mode = other
        return self.work_mode

    def query_working_mode(self, info):
        """Gets the working mode of the device.
        This tan be query mode or active mode."""
        if info[4] == '00':
            self.work_mode = "ACTIVE MODE"
        elif info[4] == '01':
            self.work_mode = "QUERY MODE"
        else:
            self.work_mode = 'UNKNOWN'
        return self.work_mode

    def query_working_period(self, info):
        """Gets the working period of the device"""
        period = int(info[4], 16)
        if period == 0:
            self.work_period = 'CONTINUOUS MODE'
        else:
            self.work_period = str(period) + ' MINUTES'
        return self.work_period

    def query_device_firmware(self, info):
        """Shows the firmware of the device"""
        firmware = ''
        count = 1
        for i in range(3, 6):
            if count == 1:
                firmware = str(int(info[3], 16))
            else:
                firmware = firmware + '-' + str(int(info[i], 16))
            count += 1
        self.firmware = firmware
        return self.firmware

    def query_device_status(self, info):
        """Shows if the device is in working mode
        or in sleep mode."""
        if info[4] == '00':
            device_status = 'SLEEPING'
        elif info[4] == '01':
            device_status = 'WORKING'
        else:
            device_status = 'working or sleeping, WE DO NOT KNOW.'
        self.work_status = device_status
        return self.work_status

    def __str__(self):
        return 'Parameters for device ID: ' + str(self.device_id)


class EPATable(object):
    """An EPATable is a table with values for AQI calculation"""
    def __init__(self):
        self.table_values_for_pm25_epa = (0, 12, 35.4, 55.4, 150.4, 250.4, 350.4, 500.4)
        self.table_values_for_pm10_epa = (0, 54, 154, 254, 354, 424, 504, 604)
        self.table_values_for_aqi_epa = (0, 50, 100, 150, 200, 300, 400, 500)
        self.steps_pm10 = 1.0
        self.steps_pm25 = 0.1

    def get_table_values_for_pm25_epa(self):
        return self.table_values_for_pm25_epa

    def get_table_values_for_pm10_epa(self):
        return self.table_values_for_pm10_epa

    def get_table_values_for_aqi_epa(self):
        return self.table_values_for_aqi_epa

    def get_steps_pm10(self):
        return self.steps_pm10

    def get_steps_pm25(self):
        return self.steps_pm25

    def __str__(self):
        return 'Values from US-EPA table for air quality index calculation.'

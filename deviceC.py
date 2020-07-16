class SDS011(object):
    """A class SDS011 defines the status of a particular
    SDS011 sensor."""
    def __init__(self, rawdata):
        self.rawdata = rawdata
        self.name = str(rawdata[-4] + rawdata[-3])

    def query_working_mode(self):
        """Gets the working mode of the device.
        This tan be query mode or active mode."""
        print(self.rawdata[4], type(self.rawdata[4]))
        if self.rawdata[4] == '00':
            working_mode = "ACTIVE MODE"
        elif self.rawdata[4] =='01':
            working_mode = "QUERY MODE"
        else:
            working_mode = 'UNKNOWN'
        return working_mode

    def query_working_period(self, info):
        """Gets the working period of the device"""
        period = int(info[4], 16)
        if period == 0:
            working_period = 'CONTINUOUS MODE'
        else:
            working_period = str(period) + ' MINUTES'
        return working_period

    def get_firmware(self, info):
        """Shows the firmware of the device"""
        firmware = ''
        count = 1
        for i in range(3, 6):
            if count == 1:
                firmware = str(int(info[3], 16))
            else:
                firmware = firmware + '-' + str(int(info[i], 16))
            count += 1
        return firmware

    def query_device_status(self, info):
        """Shows if the device is in working mode
        or in sleep mode."""
        if info[4] == '00':
            device_status = 'SLEEPING'
        elif info[4] == '01':
            device_status = 'WORKING'
        else:
            device_status = 'working or sleeping, WE DO NOT KNOW.'
        return device_status

    def __str__(self):
        return "You are looking at sensor: " + str(self.name)

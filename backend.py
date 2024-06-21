class SmartDevice:
    """ Base class for smart devices """
    def __init__(self):
        self.switchedOn = False

    def toggleSwitch(self):
        """ Toggle the value of self.switchedOn"""
        self.switchedOn = not self.switchedOn

    def getSwitchedOn(self):
        """ Get and return the value of self.switchedOn"""
        return self.switchedOn

class SmartPlug(SmartDevice):
    """ Smart Plug class that sets consumption rate """
    def __init__(self):
        super().__init__()
        self.consumptionRate = 0

    def getConsumptionRate(self):
        """ Get and return the value of self.consumptionRate"""
        return self.consumptionRate
    
    def setNewConsumptionRate(self, newRate):
        """ Set the value of the consumption rate"""
        if newRate >=0 and newRate <=150:
            self.consumptionRate = newRate
        else:
            raise ValueError("Invalid consumption rate. It should be between 0 and 150.")
    
    def __str__(self):
        """ set the string value of the smart plug"""
        if self.switchedOn:
            output = "Smart Plug: On {} KW".format(self.getConsumptionRate())
        else:
            output = "Smart Plug: Off 0 KW"
        return output

class SmartHeater(SmartDevice):
    """ Smart Heater class that sets consumption rate """
    def __init__(self):
        super().__init__()
        self.setting = 0

    def getSetting(self):
        """ Get and return the value of self.setting"""
        return self.setting
    
    def setNewSetting(self, newSetting):
        """ Set the new setting of the smart heater"""
        if newSetting >=0 and newSetting <=5:
            self.setting = newSetting
        else:
            raise ValueError("Invalid setting. It should be between 0 and 5.")

    def __str__(self):
        """ returns the string value of the heater"""
        if self.switchedOn:
            output = "Smart Heater: On Setting: {}".format(self.getSetting())
        else:
            output = "Smart Heater: Off Setting: 0"
        return output

def testSmartPlug():
    smartPlug = SmartPlug()

    smartPlug.toggleSwitch()
    print(smartPlug.getSwitchedOn())

    print(smartPlug.getConsumptionRate())

    smartPlug.setNewConsumptionRate(15)
    print(smartPlug.getConsumptionRate())
    print(smartPlug)
    
def testDevice():
    smartHeater = SmartHeater()
    print(smartHeater.getSwitchedOn())
    print(smartHeater.getSetting())
    smartHeater.setNewSetting(4)
    smartHeater.toggleSwitch()
    print(smartHeater.getSwitchedOn())
    print(smartHeater)

class SmartHome:
    """ smart home class that can be used to turn on or off all the devices, makes, adds and get them from the list"""
    def __init__(self):
        """ initialize the empty list"""
        self.devices = []

    def getDevices(self):
        """ get the list of devices"""
        return self.devices

    def getDeviceAt(self, index):
        """ get the device at the given index"""
        return self.devices[index]

    def addDevice(self, device):
        """ adds given device to the list"""
        self.devices.append(device)

    def toggleSwitch(self, index):
        """ toggle the switch on or off"""
        device = self.devices[index]
        if isinstance(device, SmartPlug):
            device.toggleSwitch()
        elif isinstance(device, SmartHeater):
            device.toggleSwitch()


    def turnAllOn(self):
        """ turn all devices on"""
        for device in self.devices:
            device.switchedOn = True

    def turnAllOff(self):
        """ turn all devices off """
        for device in self.devices:
            device.switchedOn = False
    
    def __str__(self):
        """ returns the string value of the smart home class"""
        output = "Smart Devices: \n"
        for device in self.devices:
            output += "{}\n".format(device)
        return output

def testSmartHome():
    smartHome = SmartHome()

    plug1 = SmartPlug()
    plug2 = SmartPlug()

    heater = SmartHeater()

    plug2.toggleSwitch()
    plug2.setNewConsumptionRate(45)

    heater.setNewSetting(3)

    smartHome.addDevice(plug1)
    smartHome.addDevice(plug2)
    smartHome.addDevice(heater)

    print(smartHome)

    smartHome.turnAllOn()

    print(smartHome)

#testSmartPlug()
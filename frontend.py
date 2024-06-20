from backend import SmartPlug, SmartHeater, SmartHome
from tkinter import *

smartHome = SmartHome()
mainWin = Tk()

def setupHome():
    """Setup the smart home devices """
    heater1 = SmartHeater()
    heater2 = SmartHeater()
    heater3 = SmartHeater()

    smartHome.addDevice(heater1)
    smartHome.addDevice(heater2)
    smartHome.addDevice(heater3)
    
    plug1 = SmartPlug()
    plug2 = SmartPlug()

    smartHome.addDevice(plug1)
    smartHome.addDevice(plug2)

def displayDevices():
    """Display the smart home devices on the screen """
    mainWin.title("Smart Home")
    numOfDevices = len(smartHome.getDevices())
    height = (100*numOfDevices)
    mainWin.geometry("500x{}".format(height))
    mainWin.resizable(False, False)

    turnAllOffBtn = Button(mainWin, text="Turn all off", command=turnAllOff)
    turnAllOffBtn.grid(row=0, column=0, padx=15, pady=10, sticky="w")

    turnAllOnBtn = Button(mainWin, text="Turn all on", command=turnAllOn)
    turnAllOnBtn.grid(row=1, column=0, padx=15, pady=10, sticky="w")

    onDevicesLabel = Label(mainWin, text="0 Devices On")
    onDevicesLabel.grid(row=numOfDevices+2, column=0, padx=10, pady=10, sticky="w")

    addDeviceBtn = Button(mainWin, text="Add Device", command=addDevice)
    addDeviceBtn.grid(row=numOfDevices+2, column=1, padx=10, pady=15, sticky="e")

    onDevices = 5

    for index in range(numOfDevices):
        device = smartHome.getDeviceAt(index)
        smartDevice = Text(mainWin, height=2, width=30)
        smartDevice.insert("1.0", str(device))
        smartDevice.grid(row=index+2, column=0, padx=10, pady=5, sticky="w")
        smartDevice.config(state="disabled")

        if device.getSwitchedOn():
            onDevices -= 1
        onDevicesLabel.config(text="{} Devices On".format(onDevices))

        def toggle(i=index, txt=smartDevice, devlvl=onDevicesLabel):
            toggleBtnSwitch(i, txt, devlvl)
            
        toggleBtn = Button(mainWin, text="Toggle this", command=toggle)
        toggleBtn.grid(row=index+2, column=1, padx=10, pady=15, sticky="e")

        def config(i=index):
            configWin(i)

        configBtn = Button(mainWin, text="Configure", command=config)
        configBtn.grid(row=index+2, column=2, padx=10, pady=15, sticky="e")

    mainWin.mainloop()

def listDevice():
    """List all devices in the smart home"""
    devicesNum = len(smartHome.getDevices())

    for deviceIndex in range(devicesNum):
        device = smartHome.getDeviceAt(deviceIndex)

        deviceTxt = Text(mainWin, height=2, width=30)
        deviceTxt.delete("1.0", END)
        deviceTxt.insert("1.0", str(device))
        deviceTxt.grid(row=deviceIndex+2, column=0, padx=10, pady=5, sticky="w")

def toggleBtnSwitch(index, smartDevice, onDevicesLabel):
    """ updates the values of the given device at the index after the toggle button"""
    smartHome.toggleSwitch(index)
    smartDevice = Text(mainWin, height=2, width=30)
    smartDevice.delete("1.0", END)
    smartDevice.insert("1.0", str(smartHome.getDeviceAt(index)))
    smartDevice.grid(row=index+2, column=0, padx=10, pady=5, sticky="w")
    updateOnDevicesLabel(onDevicesLabel)
    
def configWin(index):
    """ configure the device settings and rate for the given index"""
    configWin = Toplevel()
    configWin.geometry("400x200")
    configWin.resizable(False, False)    

    device = smartHome.getDeviceAt(index)
    configWin.title("Configure {}".format(str(device)))

    if isinstance(device, SmartPlug):
        consumptionLabel = Label(configWin, text="Enter Consumption rate (KW):")
        consumptionLabel.grid(row=0, column=0, padx=10, pady=15)

        consumptionEntry = Entry(configWin)
        consumptionEntry.insert(0, str(device.getConsumptionRate()))
        consumptionEntry.grid(row=0, column=1, padx=10, pady=15)

    elif isinstance(device, SmartHeater):
        settingLabel = Label(configWin, text="Enter Setting:")
        settingLabel.grid(row=0, column=0, padx=10, pady=15)

        settingEntry = Entry(configWin)
        settingEntry.insert(0, str(device.getSetting()))
        settingEntry.grid(row=0, column=1, padx=10, pady=15)

    def submitCmd():
        if isinstance(device, SmartPlug):
            newCons = int(consumptionEntry.get())
            device.setNewConsumptionRate(newCons)
            listDevice()
            configWin.destroy()

        elif isinstance(device, SmartHeater):
            newSet = int(settingEntry.get())
            device.setNewSetting(newSet)
            listDevice()
            configWin.destroy()

    submitBtn = Button(configWin, text="Submit", command=submitCmd)
    submitBtn.grid(row=1, column=0, padx=10, pady=15)

def addDevice():
    """ Add device to the list of devices in the smart home"""
    devWin= Toplevel()
    devWin.geometry("400x200")
    devWin.title("Add Smart Device")
    devWin.resizable(False, False)   

    def plug():
        newPlug = devEntry.get()
        newPlug = SmartPlug()
        smartHome.addDevice(newPlug)
        listDevice()
        devWin.destroy()
    def heater():
        newHeater = devEntry.get()
        newHeater = SmartHeater()
        smartHome.addDevice(newHeater)
        listDevice()
        devWin.destroy()

    plugBtn = Button(devWin, text="Add Smart Plug", command=plug)
    plugBtn.grid(row=2, column=0, padx=10, pady=15, sticky="w")

    heaterBtn = Button(devWin, text="Add Smart Plug", command=heater)
    heaterBtn.grid(row=2, column=1, padx=10, pady=15, sticky="e")

    devEntry = Entry(devWin)
    devEntry.insert(0, "")
    devEntry.grid(row=1, column=0, columnspan=1, padx=15, pady=15)

def updateOnDevicesLabel(onDevicesLabel):
    """ Update the device labels if the device is toggled on """
    onDevices = 5
    for device in smartHome.getDevices():
        if device.getSwitchedOn():
            onDevices -= 1
    onDevicesLabel.config(text="{} Devices On".format(onDevices))

def turnAllOff():
    """ command to turn all devices off """
    smartHome.turnAllOff()
    listDevice()

def turnAllOn():
    """ command to turn all devices on """
    smartHome.turnAllOn()
    listDevice()

def main():
    """ function to call all the other functions in one"""
    setupHome()
    displayDevices()

main()
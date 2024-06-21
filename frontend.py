from backend import SmartPlug, SmartHeater, SmartHome
from tkinter import *
from tkinter import messagebox

smartHome = SmartHome()
mainWin = Tk()

def setupHome():
    """Setup the smart home devices """
    heaters = [SmartHeater() for _ in range(3)]
    plugs = [SmartPlug() for _ in range(2)]

    for device in heaters + plugs:
        smartHome.addDevice(device)


def displayDevices():
    """Display the smart home devices on the screen """
    mainWin.title("Smart Home")
    numOfDevices = len(smartHome.getDevices())
    height = (100*numOfDevices)
    mainWin.geometry(f"550x{height}")
    mainWin.resizable(False, True)

    turnAllOffBtn = Button(mainWin, text="Turn all off", command=turnAllOff)
    turnAllOffBtn.grid(row=0, column=0, padx=15, pady=10, sticky="w")

    turnAllOnBtn = Button(mainWin, text="Turn all on", command=turnAllOn)
    turnAllOnBtn.grid(row=1, column=0, padx=15, pady=10, sticky="w")

    onDevicesLabel = Label(mainWin, text="0 Devices On")
    onDevicesLabel.grid(row=numOfDevices+2, column=0, padx=10, pady=10, sticky="w")

    addDeviceBtn = Button(mainWin, text="Add Device", command=addDevice)
    addDeviceBtn.grid(row=numOfDevices+2, column=1, padx=10, pady=15, sticky="e")

    onDevices = sum(device.getSwitchedOn() for device in smartHome.getDevices())
    onDevicesLabel.config(text=f"{onDevices} Devices On")

    for index, device in enumerate(smartHome.getDevices()):
        smartDevice = Text(mainWin, height=2, width=30)
        smartDevice.insert("1.0", str(device))
        smartDevice.grid(row=index+2, column=0, padx=10, pady=5, sticky="w")
        smartDevice.config(state="disabled")

        onDevices = sum(dev.getSwitchedOn() for dev in smartHome.getDevices())
        onDevicesLabel.config(text=f"{onDevices} Devices On")

        toggleBtn = Button(mainWin, text="Toggle this", command=lambda i=index, txt=smartDevice, devlvl=onDevicesLabel: toggleBtnSwitch(i, txt, devlvl))
        toggleBtn.grid(row=index+2, column=1, padx=10, pady=15, sticky="e")

        configBtn = Button(mainWin, text="Configure", command=lambda i=index: configWin(i))
        configBtn.grid(row=index+2, column=2, padx=10, pady=15, sticky="e")

        deleteDeviceBtn = Button(mainWin, text="Delete Device", command=lambda i=index: deleteDevice(i))
        deleteDeviceBtn.grid(row=index+2, column=3, padx=10, pady=15, sticky="e")

    mainWin.mainloop()

def listDevice():
    """List all devices in the smart home"""
    # Clear the main window
    for widget in mainWin.winfo_children():
        widget.destroy()
        
    numDev = len(smartHome.getDevices())

    turnAllOffBtn = Button(mainWin, text="Turn all off", command=turnAllOff)
    turnAllOffBtn.grid(row=0, column=0, padx=15, pady=10, sticky="w")

    turnAllOnBtn = Button(mainWin, text="Turn all on", command=turnAllOn)
    turnAllOnBtn.grid(row=1, column=0, padx=15, pady=10, sticky="w")

    onDevicesLabel = Label(mainWin, text="0 Devices On")
    onDevicesLabel.grid(row=numDev+2, column=0, padx=10, pady=10, sticky="w")

    addDeviceBtn = Button(mainWin, text="Add Device", command=addDevice)
    addDeviceBtn.grid(row=numDev+2, column=1, padx=10, pady=15, sticky="e")

    onDevicesLabel = Label(mainWin, text="0 Devices On")
    onDevicesLabel.grid(row=numDev+2, column=0, padx=10, pady=10, sticky="w")

    for deviceIndex, device in enumerate(smartHome.getDevices()):
        deviceTxt = Text(mainWin, height=2, width=30)
        deviceTxt.delete("1.0", END)
        deviceTxt.insert("1.0", str(device))
        deviceTxt.grid(row=deviceIndex+2, column=0, padx=10, pady=5, sticky="w")

        toggleBtn = Button(mainWin, text="Toggle this", command=lambda i=deviceIndex, txt=device, devlvl=onDevicesLabel: toggleBtnSwitch(i, txt, devlvl))
        toggleBtn.grid(row=deviceIndex+2, column=1, padx=10, pady=15, sticky="e")

        configBtn = Button(mainWin, text="Configure", command=lambda i=deviceIndex: configWin(i))
        configBtn.grid(row=deviceIndex+2, column=2, padx=10, pady=15, sticky="e")

        deleteDeviceBtn = Button(mainWin, text="Delete Device", command=lambda i=deviceIndex: deleteDevice(i))
        deleteDeviceBtn.grid(row=deviceIndex+2, column=3, padx=10, pady=15, sticky="e")

    onDevices = sum(device.getSwitchedOn() for device in smartHome.getDevices())
    onDevicesLabel.config(text=f"{onDevices} Devices On")

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
    configWin.title(f"Configure {device}")

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
        try:
            if isinstance(device, SmartPlug):
                new_rate = int(consumptionEntry.get())
                if not 0 <= new_rate <= 150:
                    raise ValueError("Consumption rate must be between 0 and 150.")
                device.setNewConsumptionRate(new_rate)
            elif isinstance(device, SmartHeater):
                new_setting = int(settingEntry.get())
                if not 0 <= new_setting <= 5:
                    raise ValueError("Setting must be between 0 and 5.")
                device.setNewSetting(new_setting)
            listDevice()
            configWin.destroy()
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))

    submitBtn = Button(configWin, text="Submit", command=submitCmd)
    submitBtn.grid(row=1, column=0, padx=10, pady=15)

def addDevice():
    """ Add device to the list of devices in the smart home"""
    devWin= Toplevel()
    devWin.geometry("400x200")
    devWin.title("Add Smart Device")
    devWin.resizable(True, True)  # Allow window resizing

    def plug():
        new_device = SmartPlug()
        smartHome.addDevice(new_device)
        devWin.destroy()
        listDevice()  # Refresh the display

    def heater():
        new_device = SmartHeater()
        smartHome.addDevice(new_device)
        devWin.destroy()
        listDevice()  # Refresh the display

    plugBtn = Button(devWin, text="Add Smart Plug", command=plug)
    plugBtn.grid(row=2, column=0, padx=10, pady=15, sticky="w")

    heaterBtn = Button(devWin, text="Add Smart Heater", command=heater)
    heaterBtn.grid(row=2, column=1, padx=10, pady=15, sticky="e")

def deleteDevice(index):
    """ Delete the last device from the list of devices in the smart home"""
    # Clear the main window
    for widget in mainWin.winfo_children():
        widget.destroy()
    if smartHome.devices:  # Check if there are any devices to delete
        del smartHome.devices[index]  # Remove the last device
        listDevice()  # Refresh the display

def updateOnDevicesLabel(onDevicesLabel):
    """ Update the device labels if the device is toggled on """
    onDevices = sum(device.getSwitchedOn() for device in smartHome.getDevices())
    onDevicesLabel.config(text=f"{onDevices} Devices On")

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
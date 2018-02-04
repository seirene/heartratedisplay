from bluepy import btle
import time

class HrmDelegate(btle.DefaultDelegate):
    pulse = 0

    def __init__(self):
        super(HrmDelegate, self).__init__()
        btle.DefaultDelegate.__init__(self)
        self.pulse = 0
        # self.pulse = 60

    def handleNotification(self, cHandle, data):
        status = int(data[0])
        # 6 connected, 22 ok
        # 4 no contact, returns last read value
        if (status == 4 or status == 6 or status == 22):
            self.pulse = int(data[1])

class Hrm(object):
    macAddress = ""
    peripheral = None
    delegate = None

    """docstring for Hrm"""
    def __init__(self, macAddress):
        super(Hrm, self).__init__()
        try:
            self.peripheral = btle.Peripheral(macAddress)
            self.delegate = HrmDelegate()
            self.peripheral.withDelegate(self.delegate)

            hrServiceId = btle.UUID("180d")
            hrService = self.peripheral.getServiceByUUID(hrServiceId)
            heartRateId = btle.UUID("2a37")
            hrCharacteristics = hrService.getCharacteristics(heartRateId)
            descriptors = hrCharacteristics[0].getDescriptors()
            descriptor = descriptors[0]
            # Notify meter to start sending hr values
            self.peripheral.writeCharacteristic(descriptor.handle, b'\1\0')
        except Exception:
            pass

    def getPulse(self):
        return self.delegate.pulse

    def run(self):
        while True:
            # Calls handleNotification()
            if self.peripheral.waitForNotifications(1.0):
                pass

"""
import usb
busses = usb.busses()
for bus in busses:
    devices = bus.devices
    for dev in devices:
        print("Device:", dev.deviceClass)
        print("  idVendor: %d (0x%04x)" % (dev.idVendor, dev.idVendor))
        print("  idProduct: %d (0x%04x)" % (dev.idProduct, dev.idProduct)) """
"""
import struct

infile_path = "/dev/input/js0"
EVENT_SIZE = struct.calcsize("llHHI")
file = open(infile_path, "rb")
event = file.read(EVENT_SIZE)
while event:
    print(struct.unpack("llHHI", event))
    (tv_sec, tv_usec, type, code, value) = struct.unpack("llHHI", event)
    event = file.read(EVENT_SIZE) """



"""

import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
     print(device.path, device.name, device.phys) """
"""
import  evdev
devices=[evdev.InputDevice(path) for path in evdev.list_devices()]
for dev in devices:
     print(dev.path)"""


import evdev
device = evdev.InputDevice('/dev/input/js0')
print(device)


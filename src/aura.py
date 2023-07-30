import hid

ASUS_ID = 0x0b05

INPUT_HID_ID = 0x5a
AURA_HID_ID = 0x5d

INITS = [
    bytearray([AURA_HID_ID,0xb9]),
    bytearray(b"]ASUS Tech.Inc."),
    bytearray([AURA_HID_ID, 0x05, 0x20, 0x31, 0, 0x08]),
    bytearray(b"^ASUS Tech.Inc."),
    bytearray([0x5e, 0x05, 0x20, 0x31, 0, 0x08]),
]

MESSAGE_SET = bytes([AURA_HID_ID, 0xb5, 0, 0, 0])
MESSAGE_APPLY = bytes([AURA_HID_ID, 0xb4])

DEVICE_IDS = [0x1a30, 0x1854, 0x1869, 0x1866, 0x19b6, 0x1822, 0x1837, 0x1854, 0x184a, 0x183d, 0x8502, 0x1807, 0x17e0, 0x18c6, 0x1abe]

MSG = bytearray([
    AURA_HID_ID, 0xb3,
    0x00,  # Zone
    0,     # static
    0xff,  # R1
    0xff,  # G1
    0xff,  # B1
    0xe1,  # default speed
    0,     # aura.direction
    0,     # R2
    0,     # G2
    0,     # B2
    0,0,0,0,
])

def aura_devices()->list[hid.device]:
    aura_devices = []

    devices = hid.enumerate(ASUS_ID)
    for device in [d for d in devices if d["product_id"] in DEVICE_IDS]:    
        handle = hid.device()
        handle.open_path(device["path"])
        for init in INITS:
            handle.send_feature_report(init)
            if handle.error() == "Success":
                aura_devices.append(handle)
                break
        else:
            handle.close()
                
    return aura_devices

def aura_msg(r,g,b)->bytearray:
    msg = MSG.copy()
    msg[4] = r
    msg[5] = g
    msg[6] = b
    return msg

class AuraUsb:
    devices = []
    color = [0x00,0x00,0x00]

    def __init__(self):
        self.devices = aura_devices()

    def close(self):
        for device in self.devices:
            device.close()

    def set_color(self,r,g,b):
        msg = aura_msg(r,g,b)
        for device in self.devices:
            device.send_feature_report(msg)
            device.send_feature_report(MESSAGE_APPLY)
        self.color = [r,g,b]
        

        
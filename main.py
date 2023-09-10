import evdev
import time
import asyncio
from pywizlight import wizlight, PilotBuilder, discovery
#
mapper = {
    24: ["wiz-1-0"]
}

async def turn_off_light():
    light = wizlight("192.168.1.223")
    await light.turn_off()

def get_ir_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if (device.name == "gpio_ir_recv"):
            print("Using device", device.path)
            return device
    print("No device found!")

dev = get_ir_device()

async def main():
    while True:
        try:
            events = dev.read()
            if events:
                button = list(events)[0].value
                # print("Received commands", event.value)
                if button in mapper:
                    print(mapper[button])
                    await turn_off_light()
                time.sleep(1)
        except BlockingIOError:
            pass
        

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
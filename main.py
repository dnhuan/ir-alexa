import evdev
import time
import asyncio
from pywizlight import wizlight, PilotBuilder, discovery
#
mapper = {
    24: ["wiz-0-brightness-0"],
    28: ["wiz-0-brightness-1"],
    80: ["wiz-0-brightness-30"],
    84: ["wiz-0-brightness-70"],
    88: ["wiz-0-brightness-100"],

    25: ["wiz-1-brightness-0"],
    29: ["wiz-1-brightness-1"],
    81: ["wiz-1-brightness-30"],
    85: ["wiz-1-brightness-70"],
    89: ["wiz-1-brightness-100"],

    26: ["wiz-2-brightness-0"],
    30: ["wiz-2-brightness-1"],
    77: ["wiz-2-brightness-30"],
    73: ["wiz-2-brightness-70"],
    69: ["wiz-2-brightness-100"],

    64: ["wiz-0-brightness-0", "wiz-1-brightness-0", "wiz-2-brightness-0"],

    27: ["wiz-0-warmth-0", "wiz-1-warmth-0", "wiz-2-warmth-0"],
    31: ["wiz-0-warmth-20", "wiz-1-warmth-20", "wiz-2-warmth-20"],
    76: ["wiz-0-warmth-40", "wiz-1-warmth-40", "wiz-2-warmth-40"],
    72: ["wiz-0-warmth-60", "wiz-1-warmth-60", "wiz-2-warmth-60"],
    68: ["wiz-0-warmth-80", "wiz-1-warmth-80", "wiz-2-warmth-80"],
}
bulbs = []

async def send_wiz_commands(commands):
    for command in commands:
        params = command.split('-')
        light_id = int(params[1])
        ips = [bulb.ip for bulb in bulbs]
        light = wizlight(ips[light_id])

        mode = params[2]

        if mode == "brightness":
            brightness = int(params[3])
            if brightness == 0:
                await light.turn_off()
            else:
                await light.turn_on(PilotBuilder(brightness = int(brightness / 100 * 255)))
        elif mode == "warmth":
            warmth = int(params[3])
            await light.turn_on(PilotBuilder(warm_white = int(warmth / 100 * 255)))
        else:
            pass

def get_ir_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if (device.name == "gpio_ir_recv"):
            print("Using device", device.path)
            return device
    print("No device found!")

dev = get_ir_device()

async def main():
    print("Searching for light bulbs")
    global bulbs
    bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
    print("Ready")

    while True:
        try:
            events = dev.read()
            if events:
                button = list(events)[0].value
                print("Received commands", button)
                if button in mapper:
                    print(mapper[button])
                    await send_wiz_commands(mapper[button])
        except BlockingIOError:
            pass
        

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
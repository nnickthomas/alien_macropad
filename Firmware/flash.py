import time
import network
import uasyncio
import urequests

from machine import Pin

from conf import NetworkConfig, HAConfig, PicoConfig

# On-board LED
LED = Pin("LED", Pin.OUT)

# GPIO pins used for switches
SWITCHES = (
    Pin(pin_num, Pin.IN, pull=Pin.PULL_UP) for pin_num in PicoConfig.SWITCH_PINS
)

# URL to use with HA
PROTOCOL = "https://" if HAConfig.SSL else "http://"
URL = f"{PROTOCOL}{HAConfig.BASE_URL}:{HAConfig.PORT}/api/webhook/{HAConfig.WEBHOOK_BASE}"

def blink_led(amt: int, speed: float) -> None:
    """Blinks the on-board LED

    Args:
        amt (int): Amount of times to blink the LED
        speed (float): Time in seconds to wait between blinks
    """
    for _ in range(amt * 2):
        LED.toggle()
        time.sleep(speed)


def connect_to_network(timeout: int = 10) -> bool:
    """Connect to the network defined in conf.py

    Args:
        timeout (int, optional): Amount of time in seconds to wait to connect. Defaults to 10.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(NetworkConfig.SSID, NetworkConfig.PASSWORD)

    # Wait for `timeout` seconds
    while timeout > 0:
        # If successful, blink the LED three times quickly and return True
        if wlan.status() < 0 or wlan.status() >= 3:
            blink_led(3, 0.1)
            LED.off()
            return True
        timeout -= 1
        blink_led(1, 1)

    # Deactivate network adapter and return False if failure to connect
    wlan.active(False)
    return False


async def switch_listener(switch: Pin, position: int, lock: uasyncio.Lock):
    """Asyncio function for listening to switch presses

    Args:
        switch (Pin): Switch to listen to
        position (int): Position of the switch, maps to HA webhooks
        lock (uasyncio.Lock): Lock to ensure only one switch is pressed at a time
    """
    is_pressed = False
    while True:

        if switch.value() == 0 and not is_pressed and not lock.locked():
            await lock.acquire()
            is_pressed = True
            res = urequests.post(
                URL.format(key_pos = position)
            )
            res.close()
            uasyncio.sleep_ms(200)

        # Release lock and set is_pressed to False
        if is_pressed and switch.value():
            is_pressed = False
            lock.release()

        await uasyncio.sleep_ms(5)


async def run_switch_listeners(*switches: Pin):
    """Main function to drive the Pico"""
    lock = uasyncio.Lock()
    for position, switch in enumerate(switches, start=1):
        uasyncio.create_task(switch_listener(switch, position, lock))

def main():
    if not connect_to_network():
      # If the board failed to connect to the network, blink a lot
        while True:
            blink_led(1, 0.1)

    uasyncio.run(run_switch_listeners(*SWITCHES))

    loop = uasyncio.get_event_loop()
    loop.run_forever()

if __name__ == "__main__":
   main()
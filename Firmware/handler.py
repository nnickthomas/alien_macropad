import os
import time
import json
import traceback

import wifi
import board
import asyncio
import mdns as mdns_pkg

import adafruit_requests
import adafruit_connection_manager

from digitalio import DigitalInOut, Direction, Pull

from http_server import serve_http, CONFIG

LED = DigitalInOut(board.LED)
LED.direction = Direction.OUTPUT

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

def toggle_led() -> bool:
    """Toggle LED state

    Returns:
        bool: True if on, False if off
    """
    LED.value = not LED.value
    return LED.value

def blink_led(amt: int, speed: float) -> None:
    """Blinks the on-board LED

    Args:
        amt (int): Amount of times to blink the LED
        speed (float): Time in seconds to wait between blinks
    """
    for _ in range(amt * 2):
        toggle_led()
        time.sleep(speed)

def connect_to_network(ssid, password, timeout: int = 10) -> None:
    """Connect to the network defined in settings.toml

    Args:
        timeout (int, optional): Amount of time in seconds to wait to connect. Defaults to 10.
        
    Exception:
        Failing to connect will cause the onboard LED to blink repeatedly
    """
    error = None

    for _ in range(3):
        try:
            wifi.radio.connect(
                ssid=ssid,
                password=password,
                timeout=timeout
            )
            break
        except Exception as e:
            error = str(e)
    else:
        while True:
            print(error)
            blink_led(1, 0.1)
    blink_led(3, 0.1)
        
#------------------------------------------------
#                Button Functions
#------------------------------------------------
def build_request(req: dict) -> dict:
    """Build a request dict

    Args:
        req (dict): Request dict

    Returns:
        dict: Request dict
    """
    ret_dict = {
        "method": req.get("method", "GET"),
        "url": req.get("url", "http://example.com"),
        "headers": req.get('args', {}).get("headers", {}),
    }
    
    if req.get('args', {}).get("json"):
        ret_dict["json"] = req.get('args', {}).get("json")
    elif req.get('args', {}).get("data"):
        ret_dict["data"] = req.get('args', {}).get("data")
        
    return ret_dict

async def button_listener(button_conf: dict, lock: asyncio.Lock):
    """Asyncio function for listening to button presses

    Args:
        button_conf (dict): Button dict containing important information
        lock (uasyncio.Lock): Lock to ensure only one button is pressed at a time
    """
    is_pressed = False
    
    
    # Init the button
    button = DigitalInOut(
        getattr(board, f"GP{button_conf['gpio']['value']}")
    )
    button.direction = Direction.INPUT
    button.pull = Pull.UP
    
    press_count = 0
    
    async def process_button_request(exec_mode: str, button_requests: list):
        """Process button requests

        Args:
            exec_mode (str): Execution mode
            button_requests (list): List of requests
            press_count (int): Press count
        """
        
        nonlocal press_count
        
        # Used for cycle type
        req_count = len(button_requests)
        
        # Iterate through requests and execute them
        if exec_mode == 'sequence':
            for req in button_requests:
                req = build_request(req)
                res = requests.request(**req)
                if res:
                    print(res.status_code)
                    res.close()
                    
        # Cycle through requests and execute them
        elif exec_mode == 'cycle' and req_count:
            print(button_requests[press_count])
            req = build_request(button_requests[press_count])
            print(req)
            res = requests.request(**req)
            if res:
                print(res.status_code)
                res.close()
            press_count = (press_count + 1) % req_count
        
        # Blink three times if the type is invalid
        else:
            blink_led(3, 0.1)

    while True:
        # Handle button press
        if button.value == 0 and not is_pressed and not lock.locked():
            exec_mode = button_conf.get('mode', {}).get('value', 'sequence')
            button_requests = button_conf.get('requests', {}).get('value', [])
            
            await lock.acquire()
            is_pressed = True
            
            try:
                await process_button_request(exec_mode, button_requests)
            except Exception as e:
                traceback.print_exception(e)
            
            await asyncio.sleep_ms(200)

        # Release lock and set is_pressed to False
        if is_pressed and button.value:
            is_pressed = False
            lock.release()

        await asyncio.sleep_ms(5)  

async def run_button_listeners(config):
    """Function to initialize the buttons"""
    lock = asyncio.Lock()
    for button in config["buttons"]:
        asyncio.create_task(button_listener(button, lock))

def load_config():
    try:
        with open('/conf.json') as fil:
            CONFIG.update(json.load(fil))
        print("Loaded user config")
    except Exception as e:
        with open('/static/conf.json') as fil:
            CONFIG.update(json.load(fil))
        print(f"Loaded default config: {e}")
    

def running_mode(ssid, password, mdns):
    load_config()
    
    mdns_server = mdns_pkg.Server(wifi.radio)
    mdns_server.hostname = mdns
    mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=80)
        
    print("Connecting to WiFi...")
    connect_to_network(ssid, password, os.getenv('WIFI_TIMEOUT', 10))
    print("Connected to WiFi!")
        
    asyncio.run(run_button_listeners(CONFIG))
    asyncio.run(serve_http())
    loop = asyncio.get_event_loop()
    loop.run_forever()
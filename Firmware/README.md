# 👽 Alien Macropad Firmware

This directory contains the firmware for the Alien Macropad. The firmware is written in Circuitpython and is designed to run on the Pico microcontroller.

## GPIO Pinout Map 🛸

The following pins on the Pi's GPIO pinouts correspond to the following switches:

| Switch  | GPIO Pin |
| ------------- | ------------- |
| SW1  | GP5 |
| SW2  | GP6  |
| SW3  | GP4  |
| SW4  | GP7  |
| SW5  | GP3  |
| SW6  | GP8 |

Please note that odd numbered switches (SW1, SW3, SW5) share a common ground and even numbered switches (SW2, SW4, SW6) share a common ground.

## First Time Setup

To get started with the Alien Macropad, follow these steps:

1. Install the latest version of CircuitPython on the Pico. You can download the latest version of CircuitPython from the [CircuitPython website](https://circuitpython.org/board/raspberry_pi_pico/). (Note: The Alien Macropad firmware was developed using CircuitPython 9.0.4.)

2. Copy the contents of this directory to the Pico. You can do this by copying the contents of the `Firmware` directory to the `CIRCUITPY` drive on the Pico.

3. Once the files have been copied, reboot the Pico. The Alien Macropad will create a Wi-Fi access point called `AlienPad`. Connect to this access point using your computer or mobile device.

4. Once connected to the `AlienPad` access point, open a web browser and navigate to `http://192.168.4.1`. You will be prompted to select the SSID and enter the password for your Wi-Fi network. Enter the SSID and password and click `Connect`.

5. (Optional) If you want to configure an MDNS name for the Alien Macropad, you can do so by entering the desired name in the `MDNS Name` field before clicking `Connect`.

6. Once you have connected to your Wi-Fi network, the Alien Macropad will reboot and connect to the network. You can now access the Alien Macropad by navigating to `http://<mdns_name>.local` or `http://<ip_address>` in your web browser. The default MDNS name is `alienpad.local`.

## ☄️ Configuration

The Alien Macropad buttons are configured via the web interface. Unless you have deviated from the provided gerber files, the default layout in the web interface should match the physical layout of the Alien Macropad.

### 🚀 Buttons

Each key can be configured to action something different. This supports multiple actions per key, and toggling funtionality.

The Alien Macropad firmware supports all types of HTTP requests:

For both types of requests, the following parameters can be configured:

 - url: The URL to send the request to
 - json: A JSON payload to include in the request
 - headers: A dictionary of headers to include in the request
 - data: The data to include in the request body

### 🌟 Sequence Mode

In sequence mode, each button press sends a sequence of requests to the configured URLs, in the order the requests are defined. Once all requests in the sequence have been sent, the button will no longer send any requests until it is pressed again.

To use sequence mode, set the "mode" value to "sequence", then add your requests underneath it.

### 🌓 Cycle Mode

In cycle mode, each button press sends a single request defined in under 'request' one at a time, waiting for a new button press before sending the next. Once it reaches the end it will loop back to the beginning.

To use cycle mode, set the "mode" value to "cycle", then add your requests underneath it.
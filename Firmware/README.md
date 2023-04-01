# 👽 Alien Macropad Firmware

This directory contains the firmware for the Alien Macropad. The firmware is written in Python and is designed to run on the Pico microcontroller.

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

## ☄️ Configuration

The conf.json file in this directory is used to configure the macro buttons on the Alien Macropad. The configuration file contains two sections: network and buttons.

`conf.json` has the following configuration options:

```js
{
    "network": {
        "ssid": str,
        "password": str,
        Optional("timeout"): int
    },
    "buttons": [
        {
            "gpio": int,
            Optional("type"): str['sequence', 'cycle']
            "requests": [
                {
                "method": str,
                "url": str,
                Optional("data"): dict,
                Optional("json"): dict,
                Optional("headers"): dict,
                Optional("params"): dict,
                Optional("files"): dict,
                }
            ]
        }
    ]
}
```

### 📡 Network
The network section of the configuration file is used to configure the Wi-Fi network that the Alien Macropad will connect to. It has the following options:

- ssid: The name of the Wi-Fi network.
- password: The password for the Wi-Fi network.
- timeout: The amount of time (in seconds) to wait for a connection to the Wi-Fi network.

Here's an example network section of the configuration file:

    json

    "network": {
        "ssid": "my_wifi_network",
        "password": "my_wifi_password",
        "timeout": 10
    }

### 🚀 Buttons

Each key (can be configured to action something different. This supports multiple actions per key, and toggling funtionality.

The Alien Macropad firmware supports the following types of HTTP requests:
 - GET request
 - POST request

For both types of requests, the following parameters can be configured:

 - url: The URL to send the request to
 - headers: A dictionary of headers to include in the request
 - params: A dictionary of parameters to include in the request
 - data: The data to include in the request body

### 🌟 Sequence Mode

In sequence mode, each button press sends a sequence of requests to the configured URLs, in the order they are defined in the conf.json file. Once all requests in the sequence have been sent, the button will no longer send any requests until it is pressed again.

To use sequence mode, set the "mode" value for each button to "sequence", and define an array of requests in the "requests" field for each button.

Here's an example configuration for a button in sequence mode:


    {
        "gpio": 5,
        "mode": "sequence",
        "requests": [
            {
                "method": "GET",
                "url": "https://example.com/endpoint1"
            },
            {
                "method": "POST",
                "url": "https://example.com/endpoint2",
                "data": {
                    "key": "value"
                }
            }
        ]
    }

This button is configured to send a GET request to "https://example.com/endpoint1", followed by a POST request to "https://example.com/endpoint2" with the JSON data {"key": "value"}.

### 🌓 Cycle Mode

In cycle mode, each button press sends a single request to a URL defined in the conf.json file. Each button press cycles through the defined URLs in order, looping back to the first URL after the last one has been sent.

To use cycle mode, set the "mode" value for each button to "cycle", and define an array of URLs in the "urls" field for each button.

Here's an example configuration for a button in cycle mode:

    {
        "gpio": 6,
        "mode": "cycle",
        "urls": [
            "https://example.com/endpoint1",
            "https://example.com/endpoint2",
            "https://example.com/endpoint3"
        ]
    }

This button is configured to send a request to "https://example.com/endpoint1" on the first press, "https://example.com/endpoint2" on the second press, "https://example.com/endpoint3" on the third press, and then back to "https://example.com/endpoint1" on the fourth press, and so on.


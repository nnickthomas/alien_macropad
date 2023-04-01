
# 👽Alien Macropad

A DIY standalone macropad using the Raspberry Pi Pico W for homeassistant, twitch, or anything.

![GitHub](https://img.shields.io/github/license/nnickthomas/alien_macropad) ![GitHub Repo stars](https://img.shields.io/github/stars/nnickthomas/alien_macropad?style=social)

👽 🐄 🛸 ⭐ 🌙 🪐

them big green aliens they came them gone they took my cows

## Features 🐄

- Designed for the Pi Pico W
- Standalone device, not a keypad
- Open Source PCB designs (all files required to print your own PCB)
- Fits cherry-style switches (either plate or pcb mount)


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
## Assembly ⭐

The alien macropad requires the following components:

| Component  | Amount |
| ------------- | ------------- |
| Cherry Style Switches | 6x |
| Raspberry Pi Pico W  | 1x  |
| Alien Macropad PCB  | 1x  |
| Top Sandwich Plate  | 1x  |
| Bottom Sandwich Plate  | 1x |
| Adhesive Rubber Feet  | 4x |

The following steps detail how to assemble the device:

1) Place the PI into the U1 slot on the PCB and solder into place from the top. Please note that it may be easier for some people to perform the installation step at this phase as the Boostel button will be partially covered by the top sandwich!
2) Place the Top Sandwich Plate on top
3) Insert switches SW1-SW6 into the slots and solder into place from the bottom.
4) Place the Bottom Sandwich Plate and secure the sandwich(top plate, PCB, bottom plate)!
5) Proceed to Installation!


## Installation 🌙

This section will detail how to install the Alien Macropad software onto the now connected Pi Pico W. Please note this has not yet been tested! Also see the official [Raspberry Pi Documentation](https://projects.raspberrypi.org/en/projects/get-started-pico-w/)

   1) Download the latest version of the alien macropad. There will be two files inside (main.py and conf.json)
   2) Set your wi-fi credentials in conf.json. Create your actions in conf.json (see the [firmware documentation](https://github.com/nnickthomas/alien_macropad/tree/main/Firmware).
   3) Connect the microUSB cable to the Pi Pico W.
   4) While holding down the "Boostel" button on the PICO, connect the device to another computer.
   5) Copy the main.py file, and your modified conf.json onto the pi into the now opened directory. The file manager will open automatically on Windows and the files can be dragged over.
   6) Download the correct [firmware](https://rpf.io/pico-w-firmware) for the Pi Pico W. The regular Pi Pico has not been tested.
   7) Copy the firmware file above onto the opened directory.


    **_NOTE:_**  It is critical to add main.py and conf.json before the pico firmware!
    
## Configuration 🪐

The Alien Macropad uses a JSON file to configure functionality. The JSON file is also where the wi-fi credentials are set.

For instructions on how to configure the device, see the [firmware]((https://github.com/nnickthomas/alien_macropad/tree/main/Firmware)) section.

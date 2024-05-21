import os

import wifi
import board
import digitalio
import storage

from ipaddress import IPv4Address

# Press button attached to GP5 to enter setup mode
setup_switch = digitalio.DigitalInOut(
        getattr(board, f"GP5")
    )

setup_switch.direction = digitalio.Direction.INPUT
setup_switch.pull = digitalio.Pull.UP

# Press button attached to GP6 to switch between read-only and read/write filesystem
filesystem_switch = digitalio.DigitalInOut(
        getattr(board, f"GP6")
    )

filesystem_switch.direction = digitalio.Direction.INPUT
filesystem_switch.pull = digitalio.Pull.UP


# If the switch pin is connected to ground CircuitPython can write to the drive
storage.remount("/", readonly = 1 - filesystem_switch.value)

os.environ['MODE'] = 'running'
if setup_switch.value == 0:
    os.environ['MODE'] = 'setup'



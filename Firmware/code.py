import os
import json
import supervisor

from setup import setup_mode
from handler import running_mode

supervisor.set_next_code_file(filename = 'code.py', reload_on_error = False, reload_on_success = False)
supervisor.runtime.autoreload = False

if __name__ == '__main__':
    if os.getenv('MODE') == 'setup':
        setup_mode()
    else:
        try:
            with open('/wifi.json') as fil:
                wifi_config = json.load(fil)
                running_mode(**wifi_config)
        except Exception as e:
            setup_mode()
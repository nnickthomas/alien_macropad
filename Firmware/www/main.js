let jsonData;

document.addEventListener('alpine:init', async () => {
    console.log('Alpine initialized')

    Alpine.store('configPanel', {
        open: false,
        selectedButton: undefined,
        buttonData: undefined,
        modButtonData: undefined,
        parsedButtonData: undefined,

        toggle() {
            this.open = !this.open
        },

        openPanel(selectedButton) {
            console.log('openPanel', selectedButton)
            this.selectedButton = selectedButton;
            this.filterButtonDataGetButtonTree(selectedButton);
            console.log('buttonData', this.parsedButtonData);
            this.open = true;
        },

        filterButtonDataGetButtonTree(buttonValue) {
            const button = Alpine.store('configInfo').data.buttons.find(btn => btn.gpio.value === buttonValue);

            if (!button) {
                return null; // Button not found
            }
            // TODO This needs to be dynamic
            this.buttonData = button;
            this.modButtonData = button;

            this.parsedButtonData = JSON.stringify(this.buttonData, null, 2);
        },

        addRequest() {
            const button = Alpine.store('configPanel').modButtonData;
            console.log(button);

            let buttonToAddRequest = this.modButtonData.requests.value;
            buttonToAddRequest.push({
                method: 'GET', url: '', args: {
                    data: {}, json: {}, headers: {}
                }
            });
            console.log(button);
        },

        removeRequest(index) {
            const button = Alpine.store('configPanel').modButtonData;
            console.log(button);

            let buttonToAddRequest = this.modButtonData.requests.value;
            buttonToAddRequest.splice(index, 1);
            console.log(button);
        }
    });
    Alpine.store('configInfo', {
        resetData: {},
        data: {},

        fetchConfigData() {
            fetch('/config')
                .then(response => response.json())
                .then(configData => {
                    console.log(configData);
                    this.resetData = JSON.parse(JSON.stringify(configData));
                    this.data = configData;
                    jsonData = configData;
                    window.config = configData;
                });
        },

        saveConfigData() {
            fetch('/config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.data)
            })
        },

        checkIfChanged() {
            
        }


    });
    Alpine.store('configInfo').fetchConfigData();
    Alpine.store('networks', {
        networks: [],
        selected_network: undefined,
        selected_network_password: undefined,
        chosen_mdns: "alienpad",
        network_open: false,
        connected: false,
        fetchNetworks() {
            fetch('/wifi_networks')
                .then(response => response.json())
                .then(networks => {
                    console.log(networks);
                    this.networks = JSON.parse(JSON.stringify(networks));
                });
        },
        selectNetwork(network_index) {
            this.selected_network = network_index;
        },
        isOpen() {
            console.log("isOpen", this.networks[this.selected_network])
            return this.networks[this.selected_network].includes("OPEN");
        },
        connectNetwork() {
            fetch('/connect_wifi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ssid: this.networks[this.selected_network].ssid,
                    password: this.selected_network_password,
                    mdns: this.chosen_mdns
                })
            })
            .then(response => {
                console.log(response)
                if (response.ok) {
                    fetch('/reboot', {
                        method: 'POST'
                        });
                    // Reload after 20 seconds
                    // Redirect to this.mdns.local
                    this.connected = true;
                    setTimeout(() => { window.location.replace("http://" + this.chosen_mdns + ".local"); }, 15000);
                }
            })
        },
    });
    Alpine.store('networks').fetchNetworks();


    //TODO Add sanity check
    //TODO Add export method to configInfo
    //TODO Add confirmation dialog
})


function generateFormFromJson(jsonData) {
    function processProperty(prop) {
        if (typeof prop === 'string' || typeof prop === 'number' || typeof prop === 'boolean') {
            return {
                type: typeof prop, value: prop
            };
        } else if (Array.isArray(prop)) {
            return {
                type: 'array', items: prop.map(processProperty)
            };
        } else if (typeof prop === 'object') {
            const properties = [];
            for (const key in prop) {
                if (prop.hasOwnProperty(key)) {
                    properties.push({
                        label: key, value: processProperty(prop[key]), type: 'object'
                    });
                }
            }
            return {
                type: 'object', properties
            };
        }
    }

    return processProperty(jsonData);
}

// function connectMacropad() {
//     fetch('/macropad')
//         .then(response => response.json())
//         .then(macropadData => {
//             console.log(macropadData);
//         });
// }
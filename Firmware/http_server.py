import json
import asyncio

import mdns
import wifi
import storage
import microcontroller

import socketpool

from adafruit_httpserver import Server, Request, FileResponse, Response, OK_200, JSONResponse, INTERNAL_SERVER_ERROR_500


CONFIG = {}
MOUNT = storage.getmount("/")
SETUP = False

async def serve_http(setup=False):
    """Start the HTTP server and poll periodically for requests
    """
    
    global CONFIG
    global SETUP
    SETUP = setup
    
    pool = socketpool.SocketPool(wifi.radio)
    server = Server(pool, "/static", debug=True)
    
    #------------------------------------------------
    #                Root
    #------------------------------------------------

    @server.route("/")
    def root(request: Request):
        """
        Serve the default index.html file.
        """
        if SETUP:
            return FileResponse(request, "connect.html", "/www")
        return FileResponse(request, "index.html", "/www")
    
    #------------------------------------------------
    #                Information
    #------------------------------------------------

    @server.route("/config")
    def config(request: Request):
        """
        Serve the saved config file
        """
        # return FileResponse(request, "conf.json", "/static")
        return JSONResponse(request, CONFIG)

    @server.route("/config", methods="POST")
    def config(request: Request):
        """
        Accept the incoming config.json file
        """
        global CONFIG
        data = request.json()
        
        for pos, button in enumerate(data["buttons"]):
            CONFIG["buttons"][pos].update(button)
        
        if not MOUNT.readonly:
            with open("/conf.json", "w") as f:
                json.dump(CONFIG, f)
            
        return Response(request, status=OK_200)
    
    @server.route("/wifi_networks")
    def wifi_networks(request: Request):
        """
        Serve the saved config file
        """
        networks = []
        for n in wifi.radio.start_scanning_networks():
            if not n.ssid:
                continue
            network = {
                "ssid": n.ssid,
                "authmode": [str(n).split('.')[-1] for n in n.authmode],
            }
            if network not in networks:
                networks.append(network)
        wifi.radio.stop_scanning_networks()
        
        return JSONResponse(request, networks)
    
    @server.route("/connect_wifi", methods="POST")
    def connect_wifi(request: Request):
        """
        Accept the incoming config.json file
        """
        data = request.json()
        
        ssid = data.get("ssid", None)
        password = data.get("password", None)
        mdns_name = data.get("mdns", "alienpad").lower()
        
        print(f"Connecting to WiFi: {ssid}")
        
        try:
            wifi.radio.connect(ssid, password)
        except Exception as e:
            print(e)
            return JSONResponse(request, {'error': str(e)}, status=INTERNAL_SERVER_ERROR_500)
        
        print("Connected to WiFi!")
        print(f"Access your dashboard at: http://{mdns_name}.local")
        
        if not MOUNT.readonly:
            with open("/wifi.json", "w") as f:
                to_dump = {
                    "ssid": ssid,
                    "password": password,
                    "mdns": mdns_name,
                }
                json.dump(to_dump, f)
        
        return Response(request, status=OK_200)
    
    @server.route("/reboot", methods="POST")
    def reboot(request: Request):
        microcontroller.reset()
    
    #------------------------------------------------
    #                Imports
    #------------------------------------------------

    @server.route("/alpine.js")
    def alpine(request: Request):
        """
        Serve the alpine.js file
        """
        return FileResponse(request, "alpine.js", "/www")

    @server.route("/milligram.css")
    def alpine(request: Request):
        """
        Serve the milligram.css file
        """
        return FileResponse(request, "milligram.css", "/www")

    @server.route("/lodash.js")
    def alpine(request: Request):
        """
        Serve the lodash.js file
        """
        return FileResponse(request, "lodash.js", "/www")

    @server.route("/main.js")
    def alpine(request: Request):
        """
        Serve the main.js file
        """
        return FileResponse(request, "main.js", "/www")


    # Start the server
    address = wifi.radio.ipv4_address_ap or wifi.radio.ipv4_address
    server.start(str(address), 80)
    while True:
        server.poll()
        await asyncio.sleep_ms(50)
        
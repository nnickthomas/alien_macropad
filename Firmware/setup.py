import wifi
import asyncio

from http_server import serve_http

AP_SSID = "AlienPad"
    
async def start_ap(port=80):
    wifi.radio.enabled = True
    wifi.radio.start_ap(ssid=AP_SSID)

    print(f"Access point started, connect to WiFi '{AP_SSID}'")
    print(f'Visit http://{str(wifi.radio.ipv4_address_ap)}/ in your web browser')
    
    await serve_http(setup=True)
    
def setup_mode():
    asyncio.run(start_ap())
    loop = asyncio.get_event_loop()
    loop.run_forever()
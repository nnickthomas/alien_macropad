class Config:
    ...


class NetworkConfig(Config):
    SSID: str = ""
    PASSWORD: str = ""


class HAConfig(Config):
    SSL: bool = False
    BASE_URL: str = "homeassistant.local"
    PORT: str = "8123"
    WEBHOOK_BASE: str = "macropad_{key_pos}"


class PicoConfig(Config):
    SWITCH_PINS: tuple = (5, 6, 4, 7, 3, 8)

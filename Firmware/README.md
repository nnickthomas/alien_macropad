# conf.json schema

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
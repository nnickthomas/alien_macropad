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
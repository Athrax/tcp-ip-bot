import json

dict = {
    "channel": {
        "0": "Tu réponds dans un cannal discord qui n'existe pas."
    }
}
# Exporter
with open('data.json', 'w') as f:
    json.dump(dict, f)
import json

from otter.const import OTTER_CFG
from otter.util.serialize import from_json


def serialize(items):
    with open(OTTER_CFG, 'w') as file:
        json.dump(items, file, indent=2)


def deserialize():
    with open(OTTER_CFG, 'r') as f:
        string = f.read()

        if len(string) == 0:
            return dict()

        return from_json(string)

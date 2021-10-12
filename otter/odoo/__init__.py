import requests

from otter.config import deserialize


def cookies():
    config = deserialize()
    session = config['session']
    return requests.utils.cookiejar_from_dict({"session_id":session})

#encoding=utf8

import json
import time
import requests


def catchData(url):

    data = json.loads(requests.get(url=url).json()['data'])

    return data;
#encoding=utf8

import time
import uuid


def getId():
    id = uuid.uuid1().hex
    return str(id)


def getDate():
    date = time.strftime("%Y-%m-%d", time.localtime())
    return date


def printHeartbeat():
    heartbeat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(heartbeat + "---Alive")

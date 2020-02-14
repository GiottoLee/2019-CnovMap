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


def getDeltaXY(x, y):
    delta = format(float(x) - float(y), '.2f')
    delta = float(delta)
    if delta > 0 :
        return " ---> 减少 " + str(delta)
    elif delta < 0 :
        return " ---> 增加 " + str(-delta)
    else:
        return " "

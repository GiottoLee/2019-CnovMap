#encoding=utf8

import time
import schedule

from AnalysisData import *
from CatchData import catchData

if __name__ == '__main__':

    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_%d" % int(time.time() * 1000)

    data = catchData(url)

    # schedule.every(10).minutes.do(uploadData, data=data)
    # schedule.every(10).minutes.do(printData, data=data)
    # schedule.every(1).minutes.do(printHeartbeat)

    while True:
        # schedule.run_pending()
        printToday(data)
        uploadData(data)
        printHeartbeat()
        time.sleep(600)

    # printData(data)
    # uploadData(data)


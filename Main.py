#encoding=utf8

import time

from AnalysisData import *
from CatchData import catchData
from Paint import paintConfirmAddRank

if __name__ == '__main__':

    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_%d" % int(time.time() * 1000)

    data = catchData(url)

    # printData(data)
    uploadData(data)
    paintConfirmAddRank()


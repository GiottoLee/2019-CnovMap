#encoding=utf8

import json
import time

from CommonUtils import *
from DBUtils import *


def howToChange(x):
    if x > 0:
        return "增加" + str(x)
    if x < 0:
        return "减少" + str(-x)
    if x == 0:
        return "不变" + str(x)


def printData(data):
    print("上次数据更新时间" + data['lastUpdateTime'])
    print("-----------------------全国累计---------------------------")
    print("确诊总数：" + str(data['chinaTotal']['confirm']))
    print("疑似总数：" + str(data['chinaTotal']['suspect']))
    print("死亡总数：" + str(data['chinaTotal']['dead']))
    print("治愈总数：" + str(data['chinaTotal']['heal']))
    print("----------------------今日变化----------------------------")
    print("确诊 " + howToChange(data['chinaAdd']['confirm']))
    print("疑似 " + howToChange(data['chinaAdd']['suspect']))
    print("死亡 " + howToChange(data['chinaAdd']['dead']))
    print("治愈 " + howToChange(data['chinaAdd']['heal']))
    print("----------------------历史数据----------------------------")
    for chinaDay in data['chinaDayList']:
        print("=========" + "日期：" + str(chinaDay['date']) + "=========")
        print("确诊：" + str(chinaDay['confirm']))
        print("疑似：" + str(chinaDay['suspect']))
        print("死亡：" + str(chinaDay['dead']))
        print("治愈：" + str(chinaDay['heal']))
        print("死亡率：" + str(chinaDay['deadRate']))
        print("治愈率：" + str(chinaDay['healRate']))

    print("----------------------历史数据（新增/日）----------------------------")
    for chinaDayAdd in data['chinaDayAddList']:
        print("=========" + "日期：" + str(chinaDayAdd['date']) + "=========")
        print("确诊：" + str(chinaDayAdd['confirm']))
        print("疑似：" + str(chinaDayAdd['suspect']))
        print("死亡：" + str(chinaDayAdd['dead']))
        print("治愈：" + str(chinaDayAdd['heal']))
        print("单日死亡率：" + str(chinaDayAdd['deadRate']))
        print("单日治愈率：" + str(chinaDayAdd['healRate']))

    print("----------------------历史数据（每日新增）----------------------------")
    for dailyNewAdd in data['dailyNewAddHistory']:
        print("=========" + "日期：" + str(dailyNewAdd['date']) + "=========")
        print("湖北新增：" + str(dailyNewAdd['hubei']))
        print("非湖北新增：" + str(dailyNewAdd['notHubei']))
        print("全国新增：" + str(dailyNewAdd['country']))

    print("----------------------历史数据（死亡率）----------------------------")
    for dailyDead in data['dailyDeadRateHistory']:
        print("=========" + "日期：" + str(dailyDead['date']) + "=========")
        print("湖北死亡：" + str(dailyDead['hubeiDead']))
        print("湖北确诊：" + str(dailyDead['hubeiConfirm']))
        print("全国死亡：" + str(dailyDead['countryDead']))
        print("全国确诊：" + str(dailyDead['countryConfirm']))
        print("湖北死亡率：" + str(dailyDead['hubeiRate']))
        print("非湖北死亡率：" + str(dailyDead['notHubeiRate']))
        print("全国死亡率：" + str(dailyDead['countryRate']))

    print("----------------------排名（确诊增长率）----------------------------")
    for province in data['confirmAddRank']:
        print("=========" + str(data['confirmAddRank'].index(province) + 1) + "：" + province['name'] + "=========")
        print("昨日确诊数：" + province['yesterday'])
        print("前日确诊数：" + province['before'])
        print("增长率：" + province['addRate'])

    print("----------------------各省市数据----------------------------")
    for country in data['areaTree']:
        print("=========================" + country['name'] + "==============================")
        try:
            for province in country['children']:
                print("=================" + province['name'])
                print("今日新增确诊：" + str(province['today']['confirm']))
                print("今日新增疑似：" + str(province['today']['suspect']))
                print("今日新增死亡：" + str(province['today']['dead']))
                print("今日新增治愈：" + str(province['today']['heal']))
                print("确诊总数：" + str(province['total']['confirm']))
                print("疑似总数：" + str(province['total']['suspect']))
                print("死亡总数：" + str(province['total']['dead']))
                print("治愈总数：" + str(province['total']['heal']))
                print("死亡率：" + str(province['total']['deadRate']))
                print("治愈率：" + str(province['total']['healRate']))

                for city in province['children']:
                    print("=========" + city['name'])
                    print("今日新增确诊：" + str(city['today']['confirm']))
                    print("今日新增疑似：" + str(city['today']['suspect']))
                    print("今日新增死亡：" + str(city['today']['dead']))
                    print("今日新增治愈：" + str(city['today']['heal']))
                    print("确诊总数：" + str(city['total']['confirm']))
                    print("疑似总数：" + str(city['total']['suspect']))
                    print("死亡总数：" + str(city['total']['dead']))
                    print("治愈总数：" + str(city['total']['heal']))
                    print("死亡率：" + str(city['total']['deadRate']))
                    print("治愈率：" + str(city['total']['healRate']))
        except KeyError:
            print("今日新增确诊：" + str(country['today']['confirm']))
            print("今日新增疑似：" + str(country['today']['suspect']))
            print("今日新增死亡：" + str(country['today']['dead']))
            print("今日新增治愈：" + str(country['today']['heal']))
            print("确诊总数：" + str(country['total']['confirm']))
            print("疑似总数：" + str(country['total']['suspect']))
            print("死亡总数：" + str(country['total']['dead']))
            print("治愈总数：" + str(country['total']['heal']))
            print("死亡率：" + str(country['total']['deadRate']))
            print("治愈率：" + str(country['total']['healRate']))

def printToday(data):

    today = time.strftime("%m.%d")
    db = getConnection()
    cursor = db.cursor()

    cursor.execute('select updateTime '
                   'from UpdateHistory '
                   'order by updateTime desc')
    lastTime = cursor.fetchall()[1][0]

    print("数据更新时间：" + data['lastUpdateTime'])
    print("上次数据更新时间：" + lastTime)
    print("-----------------------全国累计---------------------------")

    cursor.execute('select confirm '
                   'from ChinaTotalHistory '
                   'where updateDate = %s',
                   lastTime)
    preConfirm = cursor.fetchone()[0]
    confirm = data['chinaTotal']['confirm']
    print("确诊总数：" + str(confirm) + getDeltaXY(preConfirm, confirm))


    cursor.execute('select suspect '
                   'from ChinaTotalHistory '
                   'where updateDate = %s',
                   lastTime)
    preSuspect = cursor.fetchone()[0]
    suspect = data['chinaTotal']['suspect']
    print("疑似总数：" + str(suspect) + getDeltaXY(preSuspect, suspect))


    cursor.execute('select dead '
                   'from ChinaTotalHistory '
                   'where updateDate = %s',
                   lastTime)
    preDead = cursor.fetchone()[0]
    dead = data['chinaTotal']['dead']
    print("死亡总数：" + str(dead) + getDeltaXY(preDead, dead))


    cursor.execute('select heal '
                   'from ChinaTotalHistory '
                   'where updateDate = %s',
                   lastTime)
    preHeal = cursor.fetchone()[0]
    heal = data['chinaTotal']['heal']
    print("治愈总数：" + str(heal) + getDeltaXY(preHeal, heal))


    print("----------------------今日变化----------------------------")
    print("确诊 " + howToChange(data['chinaAdd']['confirm']))
    print("疑似 " + howToChange(data['chinaAdd']['suspect']))
    print("死亡 " + howToChange(data['chinaAdd']['dead']))
    print("治愈 " + howToChange(data['chinaAdd']['heal']))

    print("-----------------------历史数据---------------------------")
    for chinaDay in data['chinaDayList']:
        if str(chinaDay['date']) == getDate():
            print("=========" + "日期：" + str(chinaDay['date']) + "=========")
            print("确诊：" + str(chinaDay['confirm']))
            print("疑似：" + str(chinaDay['suspect']))
            print("死亡：" + str(chinaDay['dead']))
            print("治愈：" + str(chinaDay['heal']))
            print("死亡率：" + str(chinaDay['deadRate']))
            print("治愈率：" + str(chinaDay['healRate']))

    print("----------------------历史数据（新增/日）----------------------------")
    for chinaDayAdd in data['chinaDayAddList']:
        # print(chinaDayAdd['date'])
        # print(today)
        if str(chinaDayAdd['date']) == today:
            print("=========" + "日期：" + str(chinaDayAdd['date']) + "=========")
            print("确诊：" + str(chinaDayAdd['confirm']))
            print("疑似：" + str(chinaDayAdd['suspect']))
            print("死亡：" + str(chinaDayAdd['dead']))
            print("治愈：" + str(chinaDayAdd['heal']))
            print("单日死亡率：" + str(chinaDayAdd['deadRate']))
            print("单日治愈率：" + str(chinaDayAdd['healRate']))

    print("----------------------历史数据（每日新增）----------------------------")
    for dailyNewAdd in data['dailyNewAddHistory']:
        # print("date" + dailyNewAdd['date'])
        # print(today)
        if dailyNewAdd['date'] == today:
            print("=========" + "日期：" + str(dailyNewAdd['date']) + "=========")
            print("湖北新增：" + str(dailyNewAdd['hubei']))
            print("非湖北新增：" + str(dailyNewAdd['notHubei']))
            print("全国新增：" + str(dailyNewAdd['country']))

    print("----------------------历史数据（死亡率）----------------------------")
    for dailyDead in data['dailyDeadRateHistory']:

        if dailyDead['date'] == today:
            print("=========" + "日期：" + str(dailyDead['date']) + "=========")
            print("湖北死亡：" + str(dailyDead['hubeiDead']))
            print("湖北确诊：" + str(dailyDead['hubeiConfirm']))
            print("全国死亡：" + str(dailyDead['countryDead']))
            print("全国确诊：" + str(dailyDead['countryConfirm']))
            print("湖北死亡率：" + str(dailyDead['hubeiRate']))
            print("非湖北死亡率：" + str(dailyDead['notHubeiRate']))
            print("全国死亡率：" + str(dailyDead['countryRate']))

    print("----------------------排名（确诊增长率）----------------------------")
    for province in data['confirmAddRank']:
        print("=========" + str(data['confirmAddRank'].index(province) + 1) + "：" + province['name'] + "=========")
        print("昨日确诊数：" + province['yesterday'])
        print("前日确诊数：" + province['before'])
        print("增长率：" + province['addRate'])

    print("----------------------各省市数据----------------------------")

    cursor.execute('select data '
                   'from WorldDailyData '
                   'where updateDate = %s',
                   lastTime)
    predata = json.loads(cursor.fetchone()[0], encoding='utf8')
    predata = predata[0]['children']
    currentData = data['areaTree'][0]['children']
    # print(predata)
    # print(currentData)

    for province in currentData:
        print("=================" + province['name'])
        for anchor in predata:
            if anchor['name'] == province['name']:

                pre = anchor['today']['confirm']
                current = province['today']['confirm']
                print("今日新增确诊：" + str(current) + getDeltaXY(pre, current))

                pre = anchor['today']['suspect']
                current = province['today']['suspect']
                print("今日新增疑似：" + str(current) + getDeltaXY(pre, current))

                pre = anchor['today']['dead']
                current = province['today']['dead']
                print("今日新增死亡：" + str(current) + getDeltaXY(pre, current))

                pre = anchor['today']['heal']
                current = province['today']['heal']
                print("今日新增治愈：" + str(current) + getDeltaXY(pre, current))

                pre = anchor['total']['confirm']
                current = province['total']['confirm']
                print("确诊总数：" + str(current) + getDeltaXY(pre, current))

                pre = anchor['total']['suspect']
                current = province['total']['suspect']
                print("疑似总数：" + str(current) + getDeltaXY(pre, current))

                pre = anchor['total']['dead']
                current = province['total']['dead']
                print("死亡总数：" + str(current) + getDeltaXY(pre, current))

                pre = anchor['total']['heal']
                current = province['total']['heal']
                print("治愈总数：" + str(current) + getDeltaXY(pre, current))

                pre = anchor['total']['deadRate']
                current = province['total']['deadRate']
                print("死亡率：" + str(current) + getDeltaXY(pre, current))

                pre = anchor['total']['healRate']
                current = province['total']['healRate']
                print("治愈率：" + str(current) + getDeltaXY(pre, current))

        # for city in province['children']:
        #     print("=========" + city['name'])
        #     print("今日新增确诊：" + str(city['today']['confirm']))
        #     print("今日新增疑似：" + str(city['today']['suspect']))
        #     print("今日新增死亡：" + str(city['today']['dead']))
        #     print("今日新增治愈：" + str(city['today']['heal']))
        #     print("确诊总数：" + str(city['total']['confirm']))
        #     print("疑似总数：" + str(city['total']['suspect']))
        #     print("死亡总数：" + str(city['total']['dead']))
        #     print("治愈总数：" + str(city['total']['heal']))
        #     print("死亡率：" + str(city['total']['deadRate']))
        #     print("治愈率：" + str(city['total']['healRate']))

    print("数据更新时间：" + data['lastUpdateTime'])
    print("上次数据更新时间：" + lastTime)



def printCurrentUpdateTime(data):

    print(data['lastUpdateTime'])



def uploadData(data):
    currentUpdateTime = data['lastUpdateTime']
    # print(currentUpdateTime)

    db = getConnection()

    # 获取上次数据更新时间
    cursor = db.cursor()
    cursor.execute('select updateTime '
                   'from UpdateHistory '
                   'where updateTime = %s',
                   currentUpdateTime)
    ifUpdate = str(cursor.fetchone())

    # 若数据有更新
    if ifUpdate == 'None':

        print("Start Update...")

        # 更新ChinaTotalHistory
        cursor.execute('insert into ChinaTotalHistory '
                       'values (%s, %s, %s, %s, %s, %s)',
                       (getId(), data['chinaTotal']['confirm'], data['chinaTotal']['suspect'],
                       data['chinaTotal']['dead'], data['chinaTotal']['heal'],
                       currentUpdateTime))
        db.commit()
        print("Update ChinaTotalHistory...")

        # 更新ChinaDayList
        for chinaDay in data['chinaDayList']:

            cursor.execute('select date '
                           'from ChinaDayList '
                           'where date = %s',
                           chinaDay['date'])
            isExist = str(cursor.fetchone())

            if isExist == 'None':
                cursor.execute('INSERT INTO ChinaDayList '
                               'VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               (getId(), chinaDay['confirm'], chinaDay['suspect'], chinaDay['dead'], chinaDay['heal'],
                                chinaDay['deadRate'], chinaDay['healRate'], chinaDay['date'], currentUpdateTime))
                db.commit()
                print("Update ChinaDayList...")



        # 更新ChinaDayAddList
        for chinaDayAdd in data['chinaDayAddList']:
            cursor.execute('select date '
                           'from ChinaDayAddList '
                           'where date = %s',
                           chinaDayAdd['date'])
            isExist = str(cursor.fetchone())

            if isExist == 'None':
                cursor.execute('INSERT INTO ChinaDayAddList '
                               'VALUE (%s, %s, %s, %s, %s, %s, %s, %s)',
                               (getId(), chinaDayAdd['confirm'], chinaDayAdd['suspect'], chinaDayAdd['dead'],
                                chinaDayAdd['deadRate'], chinaDayAdd['healRate'], chinaDayAdd['date'],
                                currentUpdateTime))
                db.commit()
                print("Update ChinaDayAddList...")

        # 更新DailyNewAddHistory
        for dailyNewAdd in data['dailyNewAddHistory']:
            cursor.execute('SELECT date '
                           'FROM DailyNewAddHistory '
                           'WHERE date = %s',
                           dailyNewAdd['date'])
            isExist = str(cursor.fetchone())

            if isExist == 'None':
                cursor.execute('INSERT INTO DailyNewAddHistory '
                               'VALUE (%s, %s, %s, %s, %s, %s)',
                               (getId(), dailyNewAdd['date'], dailyNewAdd['hubei'],
                                dailyNewAdd['country'], dailyNewAdd['notHubei'], currentUpdateTime))
                db.commit()
                print("Update DailyNewAddHistory...")


        # 更新DailyDeadRateHistory
        for dailyDeadRate in data['dailyDeadRateHistory']:
            cursor.execute('SELECT date '
                           'FROM DailyDeadRateHistory '
                           'WHERE date = %s',
                           dailyDeadRate['date'])
            isExist = str(cursor.fetchone())

            if isExist == 'None':
                cursor.execute('INSERT INTO DailyDeadRateHistory '
                               'VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               (getId(), dailyDeadRate['date'], dailyDeadRate['hubeiDead'],
                                dailyDeadRate['hubeiConfirm'],dailyDeadRate['countryDead'],
                                dailyDeadRate['countryConfirm'], dailyDeadRate['hubeiRate'],
                               dailyDeadRate['notHubeiRate'], dailyDeadRate['countryRate'], currentUpdateTime))
                db.commit()
                print("Update DailyDeadRateHistory...")


        # 更新ConfirmAddRank
        cursor.execute('INSERT INTO ConfirmAddRank '
                       'VALUE (%s, %s, %s)',
                       (getId(), json.dumps(data['confirmAddRank'], ensure_ascii=False), currentUpdateTime))
        db.commit()
        print("ConfirmAddRank is empty, update...")


        # 更新WorldDailyData
        cursor.execute('INSERT INTO WorldDailyData '
                       'VALUE (%s, %s, %s, %s)',
                       (getId(), json.dumps(data['areaTree'], ensure_ascii=False), getDate(), currentUpdateTime))
        db.commit()
        print("Update WorldDailyData...")


        # 写入数据更新时间
        cursor.execute('INSERT INTO UpdateHistory '
                       'VALUE (%s, %s)',
                       (getId(), currentUpdateTime))
        db.commit()
        print("Update time is writed...")
        print("Update success...")

    else:
        print("Data is latest...")





    db.close()

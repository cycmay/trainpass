# -*- coding:utf-8 -*-
__author__ = 'Bicycle'

import datetime
import random
import time

from Exceptions.ticketConfigException import TicketConfigException
from config.common import maxDate, maxRunStopTime, maxRunTime


def time_to_minutes(time_str):
    s = time_str.split(":")
    a = int(s[0]) * 60 + int(s[1])
    return a


def minutes_to_time(minutes):
    m = minutes % 60
    if m<10:
        return str(minutes / 60) + ":" + str("0"+str(m))
    else:
        return str(minutes / 60) + ":" + str(m)


def checkDate(station_dates):
    """
    检查日期是否合法
    :param station_dates:
    :return:
    """
    today = datetime.datetime.now()
    maxDay = (today + datetime.timedelta(maxDate)).strftime("%Y-%m-%d")
    for station_date in station_dates[::-1]:
        date = datetime.datetime.strftime(datetime.datetime.strptime(station_date, "%Y-%m-%d"), "%Y-%m-%d")
        if date < today.strftime("%Y-%m-%d") or date > maxDay:
            print(u"警告：当前时间配置有小于当前时间或者大于最大时间: {}, 已自动忽略".format(station_date))
            station_dates.remove(station_date)
            if not station_dates:
                print(u"当前日期设置无符合查询条件的，已被全部删除，请查证后添加!!!")
                raise TicketConfigException(u"当前日期设置无符合查询条件的，已被全部删除，请查证后添加!!!")
        else:
            station_dates[station_dates.index(station_date)] = date
    return station_dates


def checkSleepTime(session):
    now = datetime.datetime.now()
    if now.hour >= maxRunStopTime or now.hour < maxRunTime:
        print(u"12306休息时间，本程序自动停止,明天早上六点将自动运行")
        open_time = datetime.datetime(now.year, now.month, now.day, 7)
        if open_time < now:
            open_time += datetime.timedelta(1)
        time.sleep((open_time - now).seconds + round(random.uniform(1, 10)))
        session.call_login()
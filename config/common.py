# -*- coding:utf-8 -*-
__author__ = 'Bicycle'

import os
import time

rushRefreshMinTimeIntval = 2000
rushRefreshMaxTimeIntval = 3600000
rushRefreshTimeIntval = 100
# 最早运行时间
maxRunTime = 7
# 程序停止时间
maxRunStopTime = 23
# 可售天数
maxDate = 29

RS_SUC = 0
RS_TIMEOUT = 1
RS_JSON_ERROR = 2
RS_OTHER_ERROR = 3

seat_conf = {'商务座': 32,
             '一等座': 31,
             '二等座': 30,
             '特等座': 25,
             '软卧': 23,
             '硬卧': 28,
             '软座': 24,
             '硬座': 29,
             '无座': 26,
             '动卧': 33,
             }

seat_conf_2 = dict([(v, k) for (k, v) in seat_conf.items()])


def getNowTimestamp():
    return time.time()


def decMakeDir(func):
    def handleFunc(*args, **kwargs):
        dirname = func(*args, **kwargs)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        elif not os.path.isdir(dirname):
            pass

        return dirname

    return func


def getWorkDir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#
# def fileOpen(path):
#     """
#     文件读取兼容2和3
#     :param path: 文件读取路径
#     :return:
#     """
#     try:
#         with open(path, "r", ) as f:
#             return f
#     except TypeError:
#         with open(path, "r", ) as f:
#             return f



@decMakeDir
def getTmpDir():
    return os.path.join(getWorkDir(), "tmp")


@decMakeDir
def getLogDir():
    return os.path.join(getTmpDir(), "log")


@decMakeDir
def getCacheDir():
    return os.path.join(getTmpDir(), "cache")


@decMakeDir
def getVCodeDir():
    return os.path.join(getTmpDir(), "vcode")


def getVCodeImageFile(imageName):
    return os.path.join(getVCodeDir(), imageName + ".jpg")


def getCacheFile(cacheType):
    return os.path.join(getCacheDir(), cacheType + ".cache")




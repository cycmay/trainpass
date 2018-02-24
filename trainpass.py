#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.timelog import TimeLogger
import requests
import re
import time
import traceback
import os


class trainInfoGet():
    def __init__(self,station_from,station_to,date,**kwargs):
        self.station_code_url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?" \
                                "station_version=1.9045"
        self.station_from = station_from
        self.station_to = station_to
        self.date = date
        self.spcTr = kwargs['specificTrain']
        self.loger = kwargs['log']
    def getTrainsInfo(self):
        # 获取12306网站station代码信息

        try:
            date = self.date
            response = requests.get(self.station_code_url, verify=False)
            # 　使用正则表达式提取所有的站点：汉字和大写代号
            stations = dict(re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text))
            station_code_dict = dict(stations)
            # 获取站点的代码
            source = station_code_dict.get(self.station_from)
            des = station_code_dict.get(self.station_to)

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko)"
                              " Chrome63.0.3239.132 Safari/537.36",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
            query_url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO." \
                        "from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(date, source, des)
            response2 = requests.get(query_url, headers=headers, verify=False)
            row_trains = response2.json()['data']['result']
            row_trains_info = []
            for row_train in row_trains:
                # split切割之后得到的是一个列表
                data_list = row_train.split("|")
                train_no = data_list[3]
                # print(train_no)
                initial = train_no[0].lower()
                # print(train_no[0])
                # 判断是否是查询特定车次的信息
                from_station_code = data_list[6]
                to_station_code = data_list[7]
                from_station_name = ''
                to_station_name = ''
                start_time = data_list[8]
                arrive_time = data_list[9]
                time_duration = data_list[10]
                first_class_seat = data_list[31] or "--"
                second_class_seat = data_list[30] or "--"
                soft_sleep = data_list[23] or "--"
                hard_sleep = data_list[28] or "--"
                hard_seat = data_list[29] or "--"
                no_seat = data_list[33] or "--"

                _row = [train_no, self.station_from, self.station_to, start_time, arrive_time, time_duration,
                        first_class_seat, second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat]
                row_trains_info.append(_row)

            return row_trains_info

        except Exception as e:

            self.loger.timeLog(traceback.format_exc())
    def getSpecificInfo(self):
        try:
            rows = self.getTrainsInfo()
            for row in rows:
                if self.spcTr in row[0]:
                    self.loger.timeLog(row)
                    if row[8] == "有":
                        self.sendInfo("{}有二等座！".format(row[0]))
        except Exception as e:
            self.loger.timeLog(traceback.format_exc())

    def sendInfo(self, msg):
        try:
            friend = self.bot.file_helper
            friend.send(msg)
        except:
            self.loger.timeLog(traceback.format_exc())


if __name__ == '__main__':
    os.mkdir('logs')
    log = TimeLogger(logFileName="logs/train%s.log" % time.strftime("%Y_%h_%d"))
    while True:
        test = trainInfoGet("秦皇岛", "保定", "2018-02-13",specificTrain="G1284",log=log)
        #print(test.getTrainsInfo())
        test.getSpecificInfo()
        time.sleep(20)





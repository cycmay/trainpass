# -*- coding:utf-8 -*-
__author__ = 'Bicycle'

from config import urlConf
from utils.httpUrllib import HTTPClient
from utils.tipTools import time_to_minutes, minutes_to_time, checkDate
from core.LeftTicketInit import LeftTicketInit
from core.Query import query

from config.ticketConf import get_yaml
from config.common import seat_conf, seat_conf_2

import os


class TrainTicket(object):
    """
        购票类
    """

    def __init__(self):
        # 初始化
        self.from_station, self.to_station, self.station_dates, self._station_seat, self.is_more_ticket, \
        self.ticke_peoples, self.station_trains, self.ticket_black_list_time, \
        self.order_type, self.is_by_time, self.train_types, self.departure_time, \
        self.arrival_time, self.take_time, self.order_model, self.open_time, self.is_proxy = self.get_ticket_info()

        self.httpClient = HTTPClient()
        self.urls = urlConf.urls
        self.is_cdn = get_yaml()["is_cdn"]
        self.cdn_list = []
        self.queryUrl = "leftTicket/query"
        self.passengerTicketStrList = ""
        self.oldPassengerStr = ""
        self.set_type = ""

    def get_ticket_info(self):
        """
            获取配置信息
        :return:
        """

    def call_login(self, auth=False):
        """
        登录回调函数
        :return:
        """
        pass

    def station_table(self, from_station, to_station):
        """
        读取车站信息
        :param station:
        :return:
        """
        path = os.path.join(os.path.dirname(__file__), '../utils/station_name.txt')
        try:
            with open(path, encoding="utf-8") as result:
                info = result.read().split('=')[1].strip("'").split('@')
        except Exception:
            with open(path) as result:
                info = result.read().split('=')[1].strip("'").split('@')
        del info[0]
        station_name = {}
        for i in range(0, len(info)):
            n_info = info[i].split('|')
            station_name[n_info[1]] = n_info[2]
        try:
            from_station = station_name[from_station.encode("utf8")]
            to_station = station_name[to_station.encode("utf8")]
        except KeyError:
            from_station = station_name[from_station]
            to_station = station_name[to_station]
        return from_station, to_station

    def get_ticket_info(self):
        """
        获取配置信息
        :return:
        """
        ticket_info_config = get_yaml()
        from_station = ticket_info_config["set"]["from_station"]
        to_station = ticket_info_config["set"]["to_station"]
        station_dates = checkDate(ticket_info_config["set"]["station_dates"])

        set_names = ticket_info_config["set"]["set_type"]
        try:
            set_type = [seat_conf[x.encode("utf-8")] for x in ticket_info_config["set"]["set_type"]]
        except KeyError:
            set_type = [seat_conf[x] for x in ticket_info_config["set"]["set_type"]]
        is_more_ticket = ticket_info_config["set"]["is_more_ticket"]
        ticke_peoples = ticket_info_config["set"]["ticke_peoples"]
        station_trains = ticket_info_config["set"]["station_trains"]
        ticket_black_list_time = ticket_info_config["ticket_black_list_time"]
        order_type = ticket_info_config["order_type"]

        # by time
        is_by_time = ticket_info_config["set"]["is_by_time"]
        train_types = ticket_info_config["set"]["train_types"]
        departure_time = time_to_minutes(ticket_info_config["set"]["departure_time"])
        arrival_time = time_to_minutes(ticket_info_config["set"]["arrival_time"])
        take_time = time_to_minutes(ticket_info_config["set"]["take_time"])

        # 下单模式
        order_model = ticket_info_config["order_model"]
        open_time = ticket_info_config["open_time"]

        # 代理模式
        is_proxy = ticket_info_config["is_proxy"]

        print(u"*" * 50)

        if is_by_time:
            method_notie = u"购票方式：根据时间区间购票\n可接受最早出发时间：{0}\n可接受最晚抵达时间：{1}\n可接受最长旅途时间：{2}\n可接受列车类型：{3}\n" \
                .format(minutes_to_time(departure_time), minutes_to_time(arrival_time), minutes_to_time(take_time),
                        " , ".join(train_types))
        else:
            method_notie = u"购票方式：根据候选车次购买\n候选购买车次：{0}".format(",".join(station_trains))
        print(u"当前配置：\n出发站：{0}\n到达站：{1}\n乘车日期：{2}\n坐席：{3}\n是否有票优先提交：{4}\n乘车人：{5}\n" \
              u"刷新间隔: 随机(1-3S)\n{6}\n僵尸票关小黑屋时长: {7}\n下单接口: {8}\n下单模式: {9}\n预售踩点时间:{10} ".format \
                (
                from_station,
                to_station,
                station_dates,
                ",".join(set_names),
                is_more_ticket,
                ",".join(ticke_peoples),
                method_notie,
                ticket_black_list_time,
                order_type,
                order_model,
                open_time,
            ))
        print(u"*" * 50)
        return from_station, to_station, station_dates, set_type, is_more_ticket, ticke_peoples, station_trains, \
               ticket_black_list_time, order_type, is_by_time, train_types, departure_time, arrival_time, take_time, \
               order_model, open_time, is_proxy

    def main(self):
        #
        l = LeftTicketInit(self)
        l.reqLeftTicketInit()

        # 登录
        self.call_login()

        from_station, to_station = self.station_table(self.from_station, self.to_station)

        q = query(session=self,
                  from_station=from_station,
                  to_station=to_station,
                  from_station_h=self.from_station,
                  to_station_h=self.to_station,
                  _station_seat=self._station_seat,
                  station_trains=self.station_trains,
                  station_dates=self.station_dates,
                  ticke_peoples_num=len(self.ticke_peoples),
                  )
        queryResult = q.sendQuery()

        print(queryResult)
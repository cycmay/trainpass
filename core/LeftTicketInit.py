# -*- coding:utf-8 -*-
__author__ = 'Bicycle'


class LeftTicketInit(object):
    def __init__(self, session):
        # session -> 当前运行实例

        self.session = session

    def reqLeftTicketInit(self):
        """

        :return:
        """
        urls = self.session.urls["left_ticket_init"]
        self.session.httpClient.send(urls)

        return {
            "status": True,
        }
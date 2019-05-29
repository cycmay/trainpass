# -*- coding:utf-8 -*-
__author__ = 'Bicycle'

from utils import logger

from time import sleep
from collections import OrderedDict
import requests
import json
import socket


def _set_header_default():
    header_dict = OrderedDict()
    # header_dict["Accept"] = "application/json, text/plain, */*"
    header_dict["Accept-Encoding"] = "gzip, deflate"
    header_dict[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) 12306-electron/1.0.1 Chrome/59.0.3071.115 Electron/1.8.4 Safari/537.36"
    header_dict["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    header_dict["Origin"] = "https://kyfw.12306.cn"
    header_dict["Connection"] = "keep-alive"
    return header_dict


class HTTPClient(object):

    def __init__(self):
        self._cdn = None
        self._proxies = None

        self._s = requests.Session()
        self._s.headers.update(_set_header_default())

    def send(self, urls, data=None, **kwargs):
        """
            send requests
        :param urls:
        :param data:
        :param kwargs:
        :return:
        """
        allow_redirects = False
        is_logger = urls.get("is_logger", False)
        is_cdn = urls.get("is_cdn", False)
        _retry = urls.get("re_try", 0)
        _sleeptime = urls.get("s_time", 0)
        req_url = urls.get("req_url", "")

        error_data = {"code": 99999, "message": u"重试次数达到上限"}
        # 封装Header
        if data:
            method = "POST"
            self.setHeaders({"Content-Length": "{0}".format(len(data))})
        else:
            method = "GET"
            self.resetHeaders()
        # Headers里的Referer
        self.setHeadersReferer(urls["Referer"])
        # 是否记录日志文件
        if is_logger:
            logger.log(
                u"url: {0}\n传入参数: {1}\n请求方式: {2}\n".format(req_url, data, method)
            )

        self.setHeadersHost(urls["Host"])

        # cdn
        if is_cdn:
            if self._cdn:
                # print(u"当前请求cdn为{}".format(self._cdn))
                url_host = self._cdn
            else:
                url_host = urls["Host"]
        else:
            url_host = urls["Host"]

        http = urls.get("httpType") or "https"

        for i in range(_retry):
            try:
                sleep(_sleeptime)

                try:
                    requests.packages.urllib3.disable_warnings()
                except Exception as e:
                    print(e)

                response = self._s.request(
                    method=method,
                    timeout=2,
                    proxies=self._proxies,
                    url=http + "://" + url_host + req_url,
                    data=data,
                    allow_redirects=allow_redirects,
                    verify=False,
                    **kwargs
                )
                if response.status_code == 200 or response.status_code == 302:
                    if urls.get("not_decode", False):
                        return response.content
                    if response.content:
                        if is_logger:
                            logger.log(
                                u"出参: {0}".format(response.content)
                            )
                        if urls["is_json"]:
                            return json.loads(response.content.decode()) if isinstance(response.content, bytes) else response.content
                        else:
                            return response.content.decode("utf-8", "ignore") if isinstance(response.content, bytes) else response.content
                    else:
                        logger.log(
                            u"url: {0} 返回空".format(urls.get("req_url"))
                        )
                        continue
                else:
                    sleep(urls.get("re_time"))
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                pass
            except socket.error:
                pass

        print(error_data.get("massage"))
        return error_data

    def setHeaders(self, headers):
        self._s.headers.update(headers)
        return self

    def setHeadersHost(self, host):
        self._s.headers.update({"Host": host})
        return self

    def resetHeaders(self):
        self._s.headers.clear()
        self.setHeaders(_set_header_default())

    def setHeadersReferer(self, referer):
        self._s.headers.update({"Referer": referer})
        return self

    @property
    def cdn(self):
        return self._cdn

    @cdn.setter
    def cdn(self, cdn):
        self._cdn = cdn

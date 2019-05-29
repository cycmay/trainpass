# -*- coding:utf-8 -*-
__author__ = 'Bicycle'

import os
import yaml


def get_yaml():
    """
    解析yaml
    :return: s  字典
    """
    path = os.path.join(os.path.dirname(__file__) + '/ticket_config.yaml')

    with open(path, encoding="utf-8") as f:
        s = yaml.load(f)
    return s.decode() if isinstance(s, bytes) else s


if __name__ == '__main__':
    print(get_yaml())
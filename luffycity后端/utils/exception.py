#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2019/2/20 19:27'

"""
自定义的异常
"""

class PricePolicyInvalid(Exception):
    """价格策略不合法异常"""
    def __init__(self, error):
        self.error = error
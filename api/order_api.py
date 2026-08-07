# -*- coding: utf-8 -*-
"""
==================== 订单模块接口（POM 页面对象） ====================
封装订单模块的接口操作：
    - create_order() 创建订单（需要登录）
    - get_order()    查询订单详情（需要登录）
    - pay_order()    支付订单（需要登录）
====================================================================
"""
from config.config import config
from common.requests_util import requests_util


class OrderApi:
    """订单模块：下单、查单、支付"""

    def __init__(self):
        self.order_url = config.BASE_URL + "/api/order"

    def create_order(self, product_id, quantity=1):
        """
        创建订单（需要先登录）
        :param product_id: 商品 id
        :param quantity:   购买数量，默认 1
        :return: (状态码, 响应字典)
        """
        data = {"product_id": product_id, "quantity": quantity}
        return requests_util.post(self.order_url + "/create", json=data)

    def get_order(self, order_no):
        """
        查询订单详情（需要先登录）
        :param order_no: 订单号
        :return: (状态码, 响应字典)
        """
        return requests_util.get(f"{self.order_url}/{order_no}")

    def pay_order(self, order_no):
        """
        支付订单（需要先登录）
        :param order_no: 订单号
        :return: (状态码, 响应字典)
        """
        data = {"order_no": order_no}
        return requests_util.post(self.order_url + "/pay", json=data)

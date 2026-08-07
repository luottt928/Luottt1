# -*- coding: utf-8 -*-
"""
==================== 购物车模块接口（POM 页面对象） ====================
封装购物车模块的接口操作：
    - add_to_cart() 加入购物车（需要登录）
    - get_cart()    查看购物车（需要登录）
====================================================================
"""
from config.config import config
from common.requests_util import requests_util


class CartApi:
    """购物车模块：加购、查看"""

    def __init__(self):
        self.cart_url = config.BASE_URL + "/api/cart"

    def add_to_cart(self, product_id, quantity=1):
        """
        把商品加入购物车（需要先登录）
        :param product_id: 商品 id
        :param quantity:   购买数量，默认 1
        :return: (状态码, 响应字典)
        """
        data = {"product_id": product_id, "quantity": quantity}
        return requests_util.post(self.cart_url + "/add", json=data)

    def get_cart(self):
        """
        查看当前登录用户的购物车（需要先登录）
        :return: (状态码, 响应字典)
        """
        return requests_util.get(self.cart_url)

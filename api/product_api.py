# -*- coding: utf-8 -*-
"""
==================== 商品模块接口（POM 页面对象） ====================
封装商品模块的接口操作：
    - get_product_list()   商品列表
    - get_product_detail() 商品详情
====================================================================
"""
from config.config import config
from common.requests_util import requests_util


class ProductApi:
    """商品模块：列表、详情"""

    def __init__(self):
        self.list_url = config.BASE_URL + "/api/products"

    def get_product_list(self):
        """
        获取商品列表
        :return: (状态码, 响应字典)
        """
        return requests_util.get(self.list_url)

    def get_product_detail(self, product_id):
        """
        获取商品详情
        :param product_id: 商品 id
        :return: (状态码, 响应字典)
        """
        return requests_util.get(f"{self.list_url}/{product_id}")

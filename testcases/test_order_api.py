# -*- coding: utf-8 -*-
"""
==================== 订单模块测试用例 ====================
订单接口需要登录后才能调用。
================================================================
"""
from api.user_api import UserApi
from api.order_api import OrderApi

user_api = UserApi()
order_api = OrderApi()


class TestOrderApi:
    """订单模块测试"""

    def _login(self, username, password="123456"):
        """辅助方法：注册并登录"""
        user_api.register(username, password)
        user_api.login(username, password)

    def test_create_order_and_pay(self):
        """登录后下单并支付，订单状态从「待支付」变成「已支付」"""
        self._login("frank")
        # 下单：商品 1（手机）买 1 个，总价应该是 1999
        status_code, resp = order_api.create_order(1, 1)
        assert status_code == 200
        assert resp["code"] == 0
        assert resp["status"] == "待支付"
        assert resp["total_price"] == 1999.0
        order_no = resp["order_no"]

        # 按订单号查询订单
        status_code, resp = order_api.get_order(order_no)
        assert status_code == 200
        assert resp["order_no"] == order_no

        # 支付订单
        status_code, resp = order_api.pay_order(order_no)
        assert status_code == 200
        assert resp["status"] == "已支付"

    def test_create_order_out_of_stock(self):
        """库存为 0 的商品下单应该失败"""
        self._login("grace")
        # 商品 4（键盘）库存为 0
        status_code, resp = order_api.create_order(4, 1)
        assert status_code == 400
        assert resp["code"] == 2001                                     # 业务码：库存不足

    def test_create_order_without_login(self):
        """未登录时下单应该返回 401"""
        status_code, resp = order_api.create_order(1, 1)
        assert status_code == 401
        assert resp["code"] == 4001                                     # 业务码：未登录

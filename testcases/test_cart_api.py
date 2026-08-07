# -*- coding: utf-8 -*-
"""
==================== 购物车模块测试用例 ====================
注意：加购物车、查购物车都需要先登录（拿到 token）。
================================================================
"""
from api.user_api import UserApi
from api.cart_api import CartApi

user_api = UserApi()
cart_api = CartApi()


class TestCartApi:
    """购物车模块测试"""

    def _login(self, username="eve", password="123456"):
        """辅助方法：注册并登录（测试内部自己用）"""
        user_api.register(username, password)
        user_api.login(username, password)

    def test_add_to_cart_and_get(self):
        """登录后加入购物车，再查询购物车应该能查到"""
        self._login("eve")
        # 加入购物车：商品 1（手机）买 2 个
        status_code, resp = cart_api.add_to_cart(1, 2)
        assert status_code == 200
        assert resp["code"] == 0
        assert resp["cart"][0]["quantity"] == 2

        # 查询购物车
        status_code, resp = cart_api.get_cart()
        assert status_code == 200
        assert len(resp["items"]) == 1
        assert resp["items"][0]["product_id"] == 1

    def test_add_to_cart_without_login(self):
        """未登录时加入购物车应该返回 401"""
        status_code, resp = cart_api.add_to_cart(1, 1)
        assert status_code == 401
        assert resp["code"] == 4001                                     # 业务码：未登录

    def test_add_not_exist_product(self):
        """加入不存在的商品应该返回 404"""
        self._login("eve2")
        status_code, resp = cart_api.add_to_cart(999, 1)
        assert status_code == 404
        assert resp["code"] == 3001                                     # 业务码：商品不存在

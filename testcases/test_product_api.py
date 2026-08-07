# -*- coding: utf-8 -*-
"""
==================== 商品模块测试用例 ====================
商品接口是公开接口，不需要登录。
================================================================
"""
from api.product_api import ProductApi

product_api = ProductApi()


class TestProductApi:
    """商品模块测试"""

    def test_get_product_list_success(self):
        """商品列表接口应该返回至少 1 条商品"""
        status_code, resp = product_api.get_product_list()
        assert status_code == 200
        assert isinstance(resp, list)
        assert len(resp) >= 1

    def test_get_product_detail_success(self):
        """商品详情接口应该能查到 id=1 的手机"""
        status_code, resp = product_api.get_product_detail(1)
        assert status_code == 200
        assert resp["id"] == 1
        assert resp["name"] == "手机"

    def test_get_product_not_found(self):
        """查询不存在的商品应该返回 404"""
        status_code, resp = product_api.get_product_detail(999)
        assert status_code == 404
        assert resp["code"] == 3001                                     # 业务码：商品不存在

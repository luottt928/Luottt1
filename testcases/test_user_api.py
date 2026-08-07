# -*- coding: utf-8 -*-
"""
==================== 用户模块测试用例 ====================
测试用例只负责"调用接口 + 断言结果"，不关心接口怎么实现的。
================================================================
"""
from api.user_api import UserApi

# 创建用户模块的页面对象，测试用例直接用它
user_api = UserApi()


class TestUserApi:
    """用户模块测试"""

    def test_register_success(self):
        """注册新用户应该成功"""
        status_code, resp = user_api.register("alice", "123456")
        assert status_code == 200, f"注册接口状态码异常: {status_code}"
        assert resp["code"] == 0
        assert resp["msg"] == "注册成功"

    def test_register_duplicate_name(self):
        """重复注册同一个用户名应该失败"""
        user_api.register("bob", "123456")                              # 先注册一次
        status_code, resp = user_api.register("bob", "123456")          # 再注册一次
        assert status_code == 400
        assert resp["code"] == 1001                                     # 业务码：用户名已存在
        assert resp["msg"] == "用户名已存在"

    def test_login_success(self):
        """正确用户名密码登录应该成功，并返回 token"""
        user_api.register("carol", "abc123")
        status_code, resp = user_api.login("carol", "abc123")
        assert status_code == 200
        assert resp["token"]                                            # token 不为空

    def test_login_wrong_password(self):
        """密码错误时登录应该失败"""
        user_api.register("dave", "123456")
        status_code, resp = user_api.login("dave", "wrong")
        assert status_code == 401
        assert resp["code"] == 1002                                     # 业务码：用户名或密码错误

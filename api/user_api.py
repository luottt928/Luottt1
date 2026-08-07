# -*- coding: utf-8 -*-
"""
==================== 用户模块接口（POM 页面对象） ====================
什么是 POM（Page Object Model）？
    POM 本来是 UI 自动化里的设计模式：把页面上的操作封装成"页面对象"。
    做接口自动化时也可以套用这个思想：
    把"某个业务模块的所有接口操作"封装成一个类，
    测试用例只调用类的方法，不关心 URL、请求参数这些细节。

    这里就是"用户模块"的页面对象类：
    - register() 封装注册接口
    - login()    封装登录接口（成功后自动保存 token）
====================================================================
"""
from config.config import config
from common.requests_util import requests_util


class UserApi:
    """用户模块：注册、登录"""

    def __init__(self):
        # 在初始化时就把接口地址拼好，后面方法直接用
        self.register_url = config.BASE_URL + "/api/user/register"
        self.login_url = config.BASE_URL + "/api/user/login"

    def register(self, username, password):
        """
        注册新用户
        :param username: 用户名
        :param password: 密码
        :return: (状态码, 响应字典)
        """
        data = {"username": username, "password": password}
        return requests_util.post(self.register_url, json=data)

    def login(self, username, password):
        """
        登录
        :param username: 用户名
        :param password: 密码
        :return: (状态码, 响应字典)
        """
        data = {"username": username, "password": password}
        status_code, resp = requests_util.post(self.login_url, json=data)
        # 登录成功后，把 token 交给全局的 requests_util 保存，
        # 这样后面所有接口请求都会自动带上 Authorization 请求头
        if resp.get("token"):
            requests_util.set_token(resp["token"])
        return status_code, resp

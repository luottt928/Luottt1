# -*- coding: utf-8 -*-
"""
==================== 请求工具类 ====================
作用：在 requests 库的基础上再封装一层，统一管理：
    1. 请求头（自动带上 token）
    2. 请求超时时间
    3. 响应日志打印（方便调试）
以后想统一加日志、加签名、加重试等，只需要改这一个文件。
====================================================
"""
import requests
from config.config import config


class RequestsUtil:
    """封装好的请求工具类"""

    def __init__(self):
        # requests.Session 会自动管理 cookies，也能复用连接，性能更好
        self.session = requests.Session()
        # 登录后拿到的 token，初始为空
        self.token = None

    def set_token(self, token):
        """登录成功后调用，把 token 保存下来"""
        self.token = token

    def clear_token(self):
        """清空 token，一般用于每个测试用例执行前，避免用例互相影响"""
        self.token = None

    def _headers(self):
        """
        生成请求头：
        如果已经登录（有 token），就自动带上 Authorization: Bearer <token>
        """
        headers = dict(config.HEADERS)  # copy 一份，避免修改到全局配置
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        return headers

    def _parse_response(self, response):
        """把响应转换成字典，并打印日志，方便调试"""
        try:
            result = response.json()  # 转成 JSON 字典
        except Exception:
            result = response.text   # 转不了 JSON 就保留原文
        print(f"    <- 状态码: {response.status_code} | 响应: {result}")
        return result

    def get(self, url, params=None):
        """发送 GET 请求，返回 (状态码, 响应数据) 元组"""
        print(f"-> GET  {url}  参数: {params}")
        response = self.session.get(
            url,
            params=params,
            headers=self._headers(),
            timeout=config.TIMEOUT,
        )
        return response.status_code, self._parse_response(response)

    def post(self, url, json=None):
        """发送 POST 请求，返回 (状态码, 响应数据) 元组"""
        print(f"-> POST {url}  数据: {json}")
        response = self.session.post(
            url,
            json=json,
            headers=self._headers(),
            timeout=config.TIMEOUT,
        )
        return response.status_code, self._parse_response(response)

    def put(self, url, json=None):
        """发送 PUT 请求，返回 (状态码, 响应数据) 元组"""
        print(f"-> PUT  {url}  数据: {json}")
        response = self.session.put(
            url,
            json=json,
            headers=self._headers(),
            timeout=config.TIMEOUT,
        )
        return response.status_code, self._parse_response(response)

    def delete(self, url):
        """发送 DELETE 请求，返回 (状态码, 响应数据) 元组"""
        print(f"-> DELETE {url}")
        response = self.session.delete(
            url,
            headers=self._headers(),
            timeout=config.TIMEOUT,
        )
        return response.status_code, self._parse_response(response)


# 创建一个全局唯一的实例。
# 整个项目共用这一个实例，这样登录后 token 才能在所有接口之间共享。
requests_util = RequestsUtil()

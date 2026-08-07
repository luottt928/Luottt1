# -*- coding: utf-8 -*-
"""
==================== 测试用例层的 conftest.py ====================
作用：pytest 的 fixture（夹具）可以写在这里，
     本目录及子目录下的所有测试用例都能自动使用。
===============================================================
"""
import pytest
from common.mock_server import start_server, stop_server
from common.requests_util import requests_util


@pytest.fixture(scope="session", autouse=True)
def start_mock_server():
    """
    启动本地模拟服务器。
    scope="session"：整个测试会话只启动一次。
    autouse=True   ：不用手动传参，每个测试用例都会自动生效。
    """
    server = start_server()
    yield server          # 用例执行期间服务器保持运行
    stop_server(server)   # 所有用例跑完后关闭服务器


@pytest.fixture(autouse=True)
def clear_token():
    """
    每个测试用例执行前，清空登录 token。
    避免上一个用例的登录状态影响到下一个用例。
    """
    requests_util.clear_token()
    yield

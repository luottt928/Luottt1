# -*- coding: utf-8 -*-
"""
==================== 配置文件 ====================
作用：把整个项目中可能会经常变动的"全局配置"集中放在这里。
以后要改环境地址、超时时间、请求头，只需要改这一个文件即可。
==================================================
"""


class Config:
    """全局配置类"""

    # 电商平台接口的根地址（base url）
    # 说明：这里默认指向"本地模拟服务器"，不需要外网，练习时直接就能跑通。
    #      以后有真实环境了，把下面这一行换成真实地址即可，例如：
    #      BASE_URL = "https://fakestoreapi.com"
    BASE_URL = "http://127.0.0.1:8000"

    # 统一的请求头（发送 JSON 数据时需要 Content-Type）
    HEADERS = {
        "Content-Type": "application/json"
    }

    # 请求超时时间（秒），防止接口卡死导致测试一直等
    TIMEOUT = 10


# 创建一个全局的配置实例，其它模块这样用：
#   from config.config import config
#   print(config.BASE_URL)
config = Config()

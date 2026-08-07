# -*- coding: utf-8 -*-
"""
==================== 根目录 conftest.py ====================
作用：pytest 在收集用例时，会自动加载项目里的 conftest.py。
这里做一件事：把项目根目录加入 Python 的模块搜索路径，
这样测试用例里 import config / common / api 才能成功。
===========================================================
"""
import os
import sys

# 当前文件所在目录就是项目根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

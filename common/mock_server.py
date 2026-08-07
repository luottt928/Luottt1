# -*- coding: utf-8 -*-
"""
==================== 本地模拟电商服务器 ====================
作用：用 Python 自带的 http.server 模拟一个电商平台的后端接口。
好处：不需要外网、不依赖真实服务器，练习时随时都能跑通。

模拟的接口（都是电商平台的核心接口）：
    用户：  注册 /api/user/register，登录 /api/user/login
    商品：  商品列表 /api/products，商品详情 /api/products/<id>
    购物车：加入购物车 /api/cart/add，查看购物车 /api/cart
    订单：  创建订单 /api/order/create，订单详情 /api/order/<订单号>，支付 /api/order/pay
============================================================
"""
import json
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer

# -------------------- 模拟数据库（用内存里的字典代替真实数据库） --------------------
USERS = {}    # 已注册的用户: {用户名: {"user_id": id, "password": 密码}}
TOKENS = {}   # 已登录的 token: {token: 用户id}
CARTS = {}    # 购物车: {用户id: [{"product_id": 1, "quantity": 2}, ...]}
ORDERS = {}   # 订单: {订单号: 订单信息字典}

# 商品数据（模拟数据库里的一张商品表）
PRODUCTS = [
    {"id": 1, "name": "手机",       "price": 1999.0, "stock": 100},
    {"id": 2, "name": "笔记本电脑", "price": 5999.0, "stock": 50},
    {"id": 3, "name": "耳机",       "price": 299.0,  "stock": 200},
    {"id": 4, "name": "键盘",       "price": 129.0,  "stock": 0},   # 库存为 0，用来测"库存不足"
]


def _send_json(handler, status, data):
    """把字典转成 JSON 返回给客户端"""
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class MockHandler(BaseHTTPRequestHandler):
    """处理 HTTP 请求的类"""

    # 关闭默认的访问日志，让控制台干净一些
    def log_message(self, format, *args):
        pass

    def _read_json(self):
        """读取请求体并转成字典"""
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _get_login_user(self):
        """
        从请求头 Authorization 中解析 token，返回对应的用户 id。
        没登录返回 None。
        """
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[len("Bearer "):]
            return TOKENS.get(token)
        return None

    # ---------------- GET 请求处理 ----------------
    def do_GET(self):
        path = self.path

        # 1. 商品列表
        if path == "/api/products":
            _send_json(self, 200, PRODUCTS)

        # 2. 商品详情，例如 /api/products/1
        elif path.startswith("/api/products/"):
            product_id = int(path.rsplit("/", 1)[1])
            product = next((p for p in PRODUCTS if p["id"] == product_id), None)
            if product:
                _send_json(self, 200, product)
            else:
                _send_json(self, 404, {"code": 3001, "msg": "商品不存在"})

        # 3. 查看购物车（需要登录）
        elif path == "/api/cart":
            user_id = self._get_login_user()
            if not user_id:
                _send_json(self, 401, {"code": 4001, "msg": "未登录"})
            else:
                _send_json(self, 200, {"user_id": user_id, "items": CARTS.get(user_id, [])})

        # 4. 订单详情，例如 /api/order/NO123456（需要登录）
        elif path.startswith("/api/order/"):
            user_id = self._get_login_user()
            if not user_id:
                _send_json(self, 401, {"code": 4001, "msg": "未登录"})
            else:
                order_no = path.rsplit("/", 1)[1]
                order = ORDERS.get(order_no)
                if order:
                    _send_json(self, 200, order)
                else:
                    _send_json(self, 404, {"code": 3002, "msg": "订单不存在"})

        else:
            _send_json(self, 404, {"code": 9999, "msg": "接口不存在"})

    # ---------------- POST 请求处理 ----------------
    def do_POST(self):
        path = self.path
        data = self._read_json()

        # 1. 注册
        if path == "/api/user/register":
            username = data.get("username")
            password = data.get("password")
            if username in USERS:
                _send_json(self, 400, {"code": 1001, "msg": "用户名已存在"})
            else:
                user_id = len(USERS) + 1
                USERS[username] = {"user_id": user_id, "password": password}
                _send_json(self, 200, {"code": 0, "msg": "注册成功", "user_id": user_id})

        # 2. 登录
        elif path == "/api/user/login":
            username = data.get("username")
            password = data.get("password")
            user = USERS.get(username)
            if not user or user["password"] != password:
                _send_json(self, 401, {"code": 1002, "msg": "用户名或密码错误"})
            else:
                token = uuid.uuid4().hex  # 生成一个随机的 token
                TOKENS[token] = user["user_id"]
                _send_json(self, 200, {
                    "code": 0, "msg": "登录成功",
                    "token": token, "user_id": user["user_id"], "username": username,
                })

        # 3. 加入购物车（需要登录）
        elif path == "/api/cart/add":
            user_id = self._get_login_user()
            if not user_id:
                _send_json(self, 401, {"code": 4001, "msg": "未登录"})
            else:
                product_id = data.get("product_id")
                quantity = data.get("quantity", 1)
                product = next((p for p in PRODUCTS if p["id"] == product_id), None)
                if not product:
                    _send_json(self, 404, {"code": 3001, "msg": "商品不存在"})
                else:
                    # 如果购物车里已有该商品，则累加数量
                    cart = CARTS.setdefault(user_id, [])
                    for item in cart:
                        if item["product_id"] == product_id:
                            item["quantity"] += quantity
                            break
                    else:
                        cart.append({"product_id": product_id, "quantity": quantity})
                    _send_json(self, 200, {"code": 0, "msg": "已加入购物车", "cart": cart})

        # 4. 创建订单（需要登录）
        elif path == "/api/order/create":
            user_id = self._get_login_user()
            if not user_id:
                _send_json(self, 401, {"code": 4001, "msg": "未登录"})
            else:
                product_id = data.get("product_id")
                quantity = data.get("quantity", 1)
                product = next((p for p in PRODUCTS if p["id"] == product_id), None)
                if not product:
                    _send_json(self, 404, {"code": 3001, "msg": "商品不存在"})
                elif product["stock"] < quantity:
                    _send_json(self, 400, {"code": 2001, "msg": "库存不足"})
                else:
                    order_no = "NO" + str(int(time.time() * 1000))
                    order = {
                        "order_no": order_no,
                        "user_id": user_id,
                        "product_id": product_id,
                        "product_name": product["name"],
                        "quantity": quantity,
                        "total_price": product["price"] * quantity,
                        "status": "待支付",
                    }
                    ORDERS[order_no] = order
                    _send_json(self, 200, {"code": 0, "msg": "下单成功", **order})

        # 5. 支付订单（需要登录）
        elif path == "/api/order/pay":
            user_id = self._get_login_user()
            if not user_id:
                _send_json(self, 401, {"code": 4001, "msg": "未登录"})
            else:
                order_no = data.get("order_no")
                order = ORDERS.get(order_no)
                if not order:
                    _send_json(self, 404, {"code": 3002, "msg": "订单不存在"})
                else:
                    order["status"] = "已支付"
                    _send_json(self, 200, {"code": 0, "msg": "支付成功", **order})

        else:
            _send_json(self, 404, {"code": 9999, "msg": "接口不存在"})


def start_server(port=8000):
    """启动模拟服务器（在后台线程运行，不阻塞主程序），返回服务器对象"""
    server = HTTPServer(("127.0.0.1", port), MockHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"模拟服务器已启动: http://127.0.0.1:{port}")
    return server


def stop_server(server):
    """关闭模拟服务器"""
    server.shutdown()
    server.server_close()
    print("模拟服务器已关闭")


# 方便单独调试：直接运行 python common/mock_server.py 可启动服务器
if __name__ == "__main__":
    start_server()
    print("按 Ctrl+C 停止服务器")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

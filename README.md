# 接口自动化测试框架（pytest + requests）

一个适合新手学习的接口自动化测试框架，采用 **分层（POM 页面对象）** 设计，
内置一个**本地模拟电商服务器**，不需要外网、不需要真实环境，拿到就能跑。

模拟的电商核心接口：用户注册/登录、商品列表/详情、购物车、下单/查询/支付。

---

## 1. 项目结构

```
练习4/
├── requirements.txt        # 项目依赖（pytest、requests）
├── pytest.ini              # pytest 配置文件（指定用例目录、命令行参数等）
├── conftest.py             # 根目录 conftest：把项目根目录加入模块搜索路径
│
├── config/                 # 【配置层】全局配置
│   └── config.py           #   base url、请求头、超时时间
│
├── common/                 # 【公共层】封装好的通用工具
│   ├── requests_util.py    #   requests 封装：统一请求头/token/超时/日志
│   └── mock_server.py      #   本地模拟电商服务器（练习用，无需外网）
│
├── api/                    # 【接口层 / POM 页面对象】一个业务模块一个类
│   ├── user_api.py         #   用户模块：注册、登录
│   ├── product_api.py      #   商品模块：列表、详情
│   ├── cart_api.py         #   购物车模块：加购、查看
│   └── order_api.py        #   订单模块：下单、查单、支付
│
└── testcases/              # 【测试层】测试用例，只负责"调用接口 + 断言"
    ├── conftest.py         #   fixture：自动启动/关闭模拟服务器、清空 token
    ├── test_user_api.py    #   用户模块用例
    ├── test_product_api.py #   商品模块用例
    ├── test_cart_api.py    #   购物车模块用例
    └── test_order_api.py   #   订单模块用例
```

## 2. 分层设计说明（POM）

- **config 配置层**：环境地址、超时等集中管理，改一处全局生效。
- **common 公共层**：把 requests 再封装一层，统一处理 token、请求头、日志。
- **api 接口层（POM）**：每个业务模块一个类，把该模块的接口操作封装成方法，
  例如 `UserApi.login()`、`OrderApi.create_order()`。
- **testcases 测试层**：用例只调用 api 层的方法并做断言，不关心请求细节。

数据流向：`测试用例 -> api 页面对象 -> requests_util -> requests -> 服务器`

## 3. 环境准备（只需一次）

```bash
# 1. 创建虚拟环境（也可以直接用你本机的 Python）
python -m venv .venv

# 2. 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Mac / Linux:
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

> 本项目已经在 `.venv` 目录里创建好虚拟环境并装好依赖，可直接进入第 4 步。

## 4. 运行测试

在项目根目录（练习4）下执行：

```bash
# 运行全部用例（会自动启动/关闭本地模拟服务器，无需手动操作）
pytest

# 运行某一个模块
pytest testcases/test_user_api.py

# 运行某一个用例
pytest testcases/test_order_api.py::TestOrderApi::test_create_order_and_pay

# 显示 print 日志（requests_util 里打印了请求/响应日志，方便调试）
pytest -s
```

## 5. 生成 HTML 测试报告（可选）

```bash
pip install pytest-html
pytest --html=reports/report.html --self-contained-html
```

## 6. 常见问题

- **端口被占用**：模拟服务器默认占用 `127.0.0.1:8000`，如果被占用，
  修改 `common/mock_server.py` 里 `start_server(port=8000)` 的端口，
  并同步修改 `config/config.py` 里的 `BASE_URL`。
- **想对接真实接口**：把 `config/config.py` 里的 `BASE_URL` 换成真实地址即可，
  例如 `BASE_URL = "https://fakestoreapi.com"`（公开的电商模拟接口）。
- **token 失效/用例互相影响**：每个用例执行前 `conftest.py` 会自动清空 token。

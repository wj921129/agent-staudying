"""
04 - Session 持久化认证
=======================
学习要点：
  1. requests.Session() 复用连接和配置
  2. 在 Session 上设置全局 Header
  3. 封装 API 客户端类（最佳实践）
  4. Session 自动管理 Cookie
"""

import requests
from utils import section, show_json

HTTPBIN = "https://httpbin.org"

# ─────────────────────────────────────────
# 示例 1：Session 基础 — 复用连接
# ─────────────────────────────────────────
section("示例 1：Session 复用连接")

def check_httpbin(resp):
    """httpbin 服务不可用时友好提示"""
    if not resp.ok:
        print(f"  ⚠ httpbin.org 暂时不可用（{resp.status_code}），跳过。")
        return False
    return True


# Session 的好处：
#   1. 复用 TCP 连接（性能更好）
#   2. 持久化 Cookie
#   3. 全局设置 headers / auth
with requests.Session() as session:
    # 第一次请求
    r1 = session.get(f"{HTTPBIN}/get")
    # 第二次请求（复用同一个 TCP 连接）
    r2 = session.get(f"{HTTPBIN}/get")
    if check_httpbin(r1) and check_httpbin(r2):
        print(f"请求 1 状态码: {r1.status_code}")
        print(f"请求 2 状态码: {r2.status_code}")
        print("两次请求共享同一个底层连接，性能更好。")

# ─────────────────────────────────────────
# 示例 2：Session 全局 Header
# ─────────────────────────────────────────
section("示例 2：Session 全局 Header + Auth")

with requests.Session() as session:
    # 全局设置 — 之后每个请求都会带上
    session.headers.update({
        "Authorization": "Bearer my-token-abc123",
        "X-App-Version": "2.0",
        "Accept": "application/json",
    })

    # 无需每次传 headers
    r1 = session.get(f"{HTTPBIN}/headers")
    if check_httpbin(r1):
        h = r1.json()["headers"]
        print("请求 1 收到的头：")
        print(f"  Authorization  : {h.get('Authorization')}")
        print(f"  X-App-Version  : {h.get('X-App-Version')}")
        print(f"  Accept         : {h.get('Accept')}")

    # 请求级别的 headers 会合并（覆盖同名全局 header）
    r2 = session.get(f"{HTTPBIN}/headers", headers={"X-Extra": "per-request"})
    if check_httpbin(r2):
        h2 = r2.json()["headers"]
        print(f"\n请求 2 额外头 X-Extra: {h2.get('X-Extra')}")
        print(f"全局头 Authorization 仍保留: {h2.get('Authorization')}")

# ─────────────────────────────────────────
# 示例 3：Session 自动管理 Cookie
# ─────────────────────────────────────────
section("示例 3：Session Cookie 管理")

with requests.Session() as session:
    # 服务端设置 Cookie
    session.get(f"{HTTPBIN}/cookies/set/session_id/abc123")
    session.get(f"{HTTPBIN}/cookies/set/user/demo_user")

    # 查看 Session 中自动保存的 Cookie
    print("Session 中保存的 Cookie：")
    for cookie in session.cookies:
        print(f"  {cookie.name} = {cookie.value}")

    # 后续请求会自动带上这些 Cookie
    r = session.get(f"{HTTPBIN}/cookies")
    if check_httpbin(r):
        show_json(r.json(), "服务端收到的 Cookie")
    else:
        print("  Cookie 已保存在 Session 中（httpbin 不可用，跳过展示）。")

# ─────────────────────────────────────────
# 示例 4：封装 API 客户端类（最佳实践）
# ─────────────────────────────────────────
section("示例 4：封装 API 客户端类")


class APIClient:
    """
    一个可复用的 REST API 客户端。
    实际项目中，每个第三方 API 都可以封装一个这样的类。
    """

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def get(self, path: str, params: dict = None) -> dict:
        """发送 GET 请求并返回 JSON"""
        url = f"{self.base_url}{path}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, path: str, data: dict = None) -> dict:
        """发送 POST 请求并返回 JSON"""
        url = f"{self.base_url}{path}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def close(self):
        """关闭底层连接"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# 使用封装好的客户端
with APIClient(base_url=HTTPBIN, api_key="demo-key-xyz") as client:
    try:
        # GET 请求
        result = client.get("/headers")
        auth = result["headers"].get("Authorization")
        print(f"GET /headers → Authorization: {auth}")

        # POST 请求
        result = client.post("/post", data={"name": "Python", "version": "3.13"})
        print(f"POST /post   → 状态: 成功")
        print(f"  服务端收到的 JSON: {result['json']}")
    except requests.HTTPError as e:
        print(f"  ⚠ httpbin.org 暂时不可用（{e}），跳过。")

print("\n💡 封装为类的好处：")
print("   1. 初始化时配置一次 auth，后续调用无需重复传")
print("   2. 统一错误处理（raise_for_status）")
print("   3. 方便 mock 和单元测试")

print("\n✅ 本节完成！Session + API 客户端封装已掌握。")

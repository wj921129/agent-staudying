"""
03 - Auth Header 认证处理
=========================
学习要点：
  1. 自定义 Header（headers 参数）
  2. Bearer Token 认证
  3. API Key 认证（Header 方式）
  4. Basic Auth 认证
  5. httpbin 验证请求头是否正确发送
"""

import requests
from utils import section, show_json

HTTPBIN = "https://httpbin.org"

# ─────────────────────────────────────────
# 示例 1：自定义 Header 基础
# ─────────────────────────────────────────
section("示例 1：自定义 Header")

# headers 参数可以传递任意自定义请求头
headers = {
    "X-Custom-Header": "hello-python",
    "Accept-Language": "zh-CN",
}

def check_httpbin(resp):
    """httpbin 服务不可用时友好提示"""
    if not resp.ok:
        print(f"  ⚠ httpbin.org 暂时不可用（{resp.status_code}），跳过展示。")
        return False
    return True


response = requests.get(f"{HTTPBIN}/headers", headers=headers)
if check_httpbin(response):
    server_headers = response.json()["headers"]

    print("服务端收到的自定义头：")
    print(f"  X-Custom-Header : {server_headers.get('X-Custom-Header')}")
    print(f"  Accept-Language : {server_headers.get('Accept-Language')}")

# ─────────────────────────────────────────
# 示例 2：Bearer Token 认证（最常见）
# ─────────────────────────────────────────
section("示例 2：Bearer Token 认证")

# Bearer Token 是最常见的 API 认证方式
# 格式：Authorization: Bearer <your-token>
TOKEN = "my-super-secret-token-12345"

headers = {
    "Authorization": f"Bearer {TOKEN}",
}

response = requests.get(f"{HTTPBIN}/headers", headers=headers)
if check_httpbin(response):
    auth_header = response.json()["headers"].get("Authorization")
    print(f"服务端收到的 Authorization 头: {auth_header}")

# 模拟一个需要 token 的完整请求流程：
# response = requests.get(
#     "https://api.example.com/protected-resource",
#     headers={"Authorization": f"Bearer {TOKEN}"},
# )
# if response.status_code == 401:
#     print("Token 无效或已过期！")

# ─────────────────────────────────────────
# 示例 3：API Key 认证（Header 方式）
# ─────────────────────────────────────────
section("示例 3：API Key 认证")

# 很多第三方 API 使用自定义 header 传递 API Key
API_KEY = "sk-demo-abc123def456"

headers = {
    "X-API-Key": API_KEY,               # 通用写法
    # "x-api-key": API_KEY,             # 有的 API 用小写
    # "X-OpenAI-Key": API_KEY,          # 有的 API 用自定义字段名
}

response = requests.get(f"{HTTPBIN}/headers", headers=headers)
if check_httpbin(response):
    received_key = response.json()["headers"].get("X-Api-Key")
    print(f"服务端收到的 API Key: {received_key}")

print("\n💡 不同 API 的 Key 字段名不同，需查阅对应文档。")

# ─────────────────────────────────────────
# 示例 4：Basic Auth 认证
# ─────────────────────────────────────────
section("示例 4：Basic Auth 认证")

# 方式 A：使用 auth 参数（推荐，requests 自动 base64 编码）
response = requests.get(
    f"{HTTPBIN}/basic-auth/admin/password123",
    auth=("admin", "password123"),   # (用户名, 密码)
)
if check_httpbin(response):
    print(f"Basic Auth（正确密码）→ 状态码: {response.status_code}")
    print(f"响应: {response.json()}")

# 密码错误的情况（401 是预期结果）
response = requests.get(
    f"{HTTPBIN}/basic-auth/admin/password123",
    auth=("admin", "wrong-password"),
)
print(f"Basic Auth（错误密码）→ 状态码: {response.status_code}")

# 方式 B：手动构造 Authorization header（了解原理）
import base64

username = "admin"
password = "password123"
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

headers = {"Authorization": f"Basic {credentials}"}
response = requests.get(
    f"{HTTPBIN}/basic-auth/admin/password123",
    headers=headers,
)
if check_httpbin(response):
    print(f"手动 Basic Auth     → 状态码: {response.status_code}")

# ─────────────────────────────────────────
# 示例 5：Token 过期处理模式
# ─────────────────────────────────────────
section("示例 5：Token 过期 → 自动刷新模式")


def get_headers(token: str) -> dict:
    """构造带 token 的请求头"""
    return {"Authorization": f"Bearer {token}"}


def refresh_token() -> str:
    """模拟刷新 token（实际项目中这里会调用认证接口）"""
    print("  → Token 已过期，正在刷新...")
    new_token = "refreshed-token-67890"
    print(f"  → 获得新 Token: {new_token}")
    return new_token


# 模拟 token 过期 → 刷新 → 重试 的流程
current_token = "expired-token-00000"

# 第一次请求（模拟 401）
print(f"使用 Token: {current_token}")
print("  → 模拟收到 401 Unauthorized")

# 刷新并重试
current_token = refresh_token()
print(f"使用新 Token: {current_token} 重新请求")
headers = get_headers(current_token)
response = requests.get(f"{HTTPBIN}/headers", headers=headers)
if check_httpbin(response):
    print(f"  → 重试成功！状态码: {response.status_code}")
else:
    print(f"  → httpbin 不可用，但重试逻辑已演示完毕。")

print("\n✅ 本节完成！常见认证方式已全部掌握。")

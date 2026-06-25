"""
05 - 错误处理与状态码
=====================
学习要点：
  1. HTTP 状态码含义速查
  2. response.raise_for_status() 自动抛异常
  3. requests 异常体系结构
  4. 健壮的请求封装（try/except 最佳实践）
"""

import requests
from utils import section, show_json

HTTPBIN = "https://httpbin.org"

# ─────────────────────────────────────────
# 示例 1：常见 HTTP 状态码
# ─────────────────────────────────────────
section("示例 1：常见 HTTP 状态码一览")

STATUS_CODES = {
    # 2xx 成功
    200: "OK - 请求成功",
    201: "Created - 资源创建成功",
    204: "No Content - 成功但无返回体",
    # 3xx 重定向（requests 默认自动跟随）
    301: "Moved Permanently - 永久重定向",
    302: "Found - 临时重定向",
    # 4xx 客户端错误
    400: "Bad Request - 请求参数有误",
    401: "Unauthorized - 未认证（需 token）",
    403: "Forbidden - 已认证但无权限",
    404: "Not Found - 资源不存在",
    429: "Too Many Requests - 触发限流",
    # 5xx 服务端错误
    500: "Internal Server Error - 服务端崩溃",
    502: "Bad Gateway - 网关错误",
    503: "Service Unavailable - 服务不可用",
}

print("HTTP 状态码速查表：")
for code, desc in STATUS_CODES.items():
    print(f"  {code}  {desc}")

# ─────────────────────────────────────────
# 示例 2：用 httpbin 触发各种状态码
# ─────────────────────────────────────────
section("示例 2：触发不同状态码")

test_codes = [200, 201, 400, 401, 403, 404, 500]
httpbin_ok = True
for code in test_codes:
    try:
        r = requests.get(f"{HTTPBIN}/status/{code}", timeout=10)
        status = "✅" if r.ok else "❌"
        print(f"  {status} GET /status/{code} → {r.status_code} {r.reason}")
    except requests.RequestException as e:
        if httpbin_ok:
            print(f"  ⚠ httpbin.org 不可用（{type(e).__name__}），后续状态码测试跳过。")
            httpbin_ok = False

# ─────────────────────────────────────────
# 示例 3：raise_for_status() 自动抛异常
# ─────────────────────────────────────────
section("示例 3：raise_for_status()")

try:
    # 200 不会抛异常
    r = requests.get(f"{HTTPBIN}/status/200", timeout=10)
    r.raise_for_status()
    print("200 → raise_for_status() 无异常 ✓")

    # 404 会抛出 HTTPError
    r = requests.get(f"{HTTPBIN}/status/404", timeout=10)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        print(f"404 → 捕获 HTTPError: {e}")

    # 500 也会抛出 HTTPError
    r = requests.get(f"{HTTPBIN}/status/500", timeout=10)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        print(f"500 → 捕获 HTTPError: {e}")
except requests.RequestException as e:
    print(f"  ⚠ httpbin.org 不可用（{type(e).__name__}），raise_for_status 示例跳过。")

# ─────────────────────────────────────────
# 示例 4：requests 异常体系
# ─────────────────────────────────────────
section("示例 4：requests 异常继承关系")

print("""
requests.exceptions
├── RequestException         ← 所有 requests 异常的基类
│   ├── HTTPError            ← raise_for_status() 抛出（4xx / 5xx）
│   ├── ConnectionError      ← 连接失败（DNS/拒绝连接）
│   ├── Timeout              ← 请求超时
│   │   ├── ConnectTimeout   ← 连接阶段超时
│   │   └── ReadTimeout      ← 读取阶段超时
│   └── TooManyRedirects     ← 重定向次数过多
""")

# ─────────────────────────────────────────
# 示例 5：健壮的请求封装（生产级模板）
# ─────────────────────────────────────────
section("示例 5：生产级请求封装")


def safe_request(
    method: str,
    url: str,
    max_retries: int = 2,
    timeout: int = 10,
    **kwargs,
) -> dict:
    """
    健壮地发送 HTTP 请求。
    包含：超时、重试、异常分类处理。

    返回 dict: {"ok": bool, "data": ..., "error": ...}
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.request(
                method, url, timeout=timeout, **kwargs
            )
            response.raise_for_status()
            return {"ok": True, "data": response.json(), "error": None}

        except requests.HTTPError as e:
            # 4xx 客户端错误通常不需要重试
            status = e.response.status_code
            if 400 <= status < 500:
                return {
                    "ok": False,
                    "data": None,
                    "error": f"客户端错误 {status}: {e}",
                }
            # 5xx 服务端错误可以重试
            print(f"  [尝试 {attempt}/{max_retries}] 服务端错误 {status}，重试...")

        except requests.ConnectionError:
            print(f"  [尝试 {attempt}/{max_retries}] 连接失败，重试...")

        except requests.Timeout:
            print(f"  [尝试 {attempt}/{max_retries}] 请求超时，重试...")

        except requests.RequestException as e:
            return {"ok": False, "data": None, "error": f"未知请求异常: {e}"}

    return {"ok": False, "data": None, "error": "已达最大重试次数"}


# 测试 1：成功请求
print("测试 1 - 成功请求：")
result = safe_request("GET", f"{HTTPBIN}/get")
print(f"  ok={result['ok']}, 有数据={result['data'] is not None}")

# 测试 2：404 客户端错误（不重试）
print("\n测试 2 - 404 客户端错误：")
result = safe_request("GET", f"{HTTPBIN}/status/404")
print(f"  ok={result['ok']}, error={result['error']}")

# 测试 3：500 服务端错误（会重试）
print("\n测试 3 - 500 服务端错误（会重试）：")
result = safe_request("GET", f"{HTTPBIN}/status/500", max_retries=2)
print(f"  ok={result['ok']}, error={result['error']}")

# 测试 4：超时
print("\n测试 4 - 超时（delay 10s，timeout 2s）：")
result = safe_request("GET", f"{HTTPBIN}/delay/10", max_retries=1, timeout=2)
print(f"  ok={result['ok']}, error={result['error']}")

print("\n✅ 本节完成！错误处理与健壮请求封装已掌握。")

"""
04 - 错误处理与 API 配额
========================
学习要点：
  1. 常见 HTTP 错误码及含义（404 / 403 / 401）
  2. 使用 response.raise_for_status() 主动抛出异常
  3. try/except 捕获请求异常
  4. 理解 GitHub API 速率限制（Rate Limit）

API 文档：https://docs.github.com/rest/overview/resources-in-the-rest-api
"""

import requests
from utils import GITHUB_API, HEADERS, section, show_status

# ─────────────────────────────────────────
# 第 1 步：认识常见的错误状态码
# ─────────────────────────────────────────
section("第 1 步：GitHub API 常见错误码说明")

print("""
  状态码   含义
  ──────   ──────────────────────────────────────
  200      请求成功
  401      未授权（Token 无效或过期）
  403      禁止访问（配额耗尽 / 权限不足）
  404      用户或资源不存在
  422      参数格式错误
  500      GitHub 服务器内部错误
""")

# ─────────────────────────────────────────
# 第 2 步：查询一个不存在的用户（触发 404）
# ─────────────────────────────────────────
section("第 2 步：处理 404 —— 用户不存在")

fake_username = "this_user_definitely_does_not_exist_xyz_12345"
url = f"{GITHUB_API}/users/{fake_username}"

response = requests.get(url, headers=HEADERS)
show_status(response)

# 检查状态码，手动处理
if response.status_code == 404:
    error_info = response.json()
    print(f"\n❌ 用户 '{fake_username}' 不存在")
    print(f"   API 返回消息: {error_info.get('message', '无')}")
elif response.status_code == 200:
    print("✅ 用户存在")
else:
    print(f"⚠️  意外状态码: {response.status_code}")

# ─────────────────────────────────────────
# 第 3 步：使用 raise_for_status() + try/except
# ─────────────────────────────────────────
section("第 3 步：用 raise_for_status() 统一捕获异常")

def get_follower_count(username: str) -> int:
    """
    获取指定用户的 follower 数量。
    使用 try/except 处理所有可能的网络与 HTTP 错误。
    """
    url = f"{GITHUB_API}/users/{username}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        # 如果状态码不是 2xx，立即抛出 HTTPError 异常
        response.raise_for_status()

        user = response.json()
        return user.get("followers", 0)

    except requests.exceptions.HTTPError as e:
        # HTTP 错误（404、403、401 等）
        status = e.response.status_code
        if status == 404:
            print(f"  ❌ 用户 '{username}' 不存在（404）")
        elif status == 403:
            print(f"  ❌ 请求被拒绝，可能配额已耗尽（403）")
            # 读取配额重置时间
            reset_time = e.response.headers.get("X-RateLimit-Reset", "未知")
            print(f"     配额重置时间戳: {reset_time}")
        elif status == 401:
            print(f"  ❌ 认证失败，请检查 Token 是否有效（401）")
        else:
            print(f"  ❌ HTTP 错误：{status}")
        return -1

    except requests.exceptions.ConnectionError:
        # 网络连接失败（断网、DNS 解析失败等）
        print(f"  ❌ 网络连接失败，请检查网络")
        return -1

    except requests.exceptions.Timeout:
        # 请求超时（超过 timeout 秒未响应）
        print(f"  ❌ 请求超时（10 秒无响应）")
        return -1

    except requests.exceptions.RequestException as e:
        # 其他 requests 异常（兜底）
        print(f"  ❌ 未知请求错误：{e}")
        return -1


# 测试：正常用户
print("\n测试正常用户：")
count = get_follower_count("octocat")
if count >= 0:
    print(f"  ✅ octocat 有 {count} 个 followers")

# 测试：不存在的用户
print("\n测试不存在的用户：")
count = get_follower_count("this_user_definitely_does_not_exist_xyz_12345")
if count < 0:
    print("  ⚠️  获取失败（返回 -1）")

# ─────────────────────────────────────────
# 第 4 步：查看当前 API 配额状态
# ─────────────────────────────────────────
section("第 4 步：查看当前 API 速率限制")

rate_url = f"{GITHUB_API}/rate_limit"
response = requests.get(rate_url, headers=HEADERS)
show_status(response)

rate_data = response.json()

# 未认证请求的配额
core = rate_data.get("resources", {}).get("core", {})
print(f"\nCore API 配额（未认证请求）：")
print(f"  总配额    : {core.get('limit', '?')} 次/小时")
print(f"  已使用    : {core.get('used', '?')} 次")
print(f"  剩余      : {core.get('remaining', '?')} 次")
print(f"  重置时间戳: {core.get('reset', '?')}")

print("\n💡 提示：使用 Personal Access Token 认证可将配额从 60 次/小时提升至 5000 次/小时。")
print("\n✅ 本节完成！你已掌握 GitHub API 的错误处理与配额管理。")

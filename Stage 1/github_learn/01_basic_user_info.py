"""
01 - 基础 GitHub API 调用
=========================
学习要点：
  1. 使用 requests 向 GitHub API 发送 GET 请求
  2. 理解 GitHub API 必需的请求头 (User-Agent)
  3. 解析返回的用户信息 JSON
  4. 访问嵌套字段并打印

API 文档：https://docs.github.com/rest/users/users#get-a-user
"""

import requests
from utils import GITHUB_API, HEADERS, section, show_json, show_status

# ─────────────────────────────────────────
# 第 1 步：发送请求获取用户信息
# ─────────────────────────────────────────
section("第 1 步：向 GitHub API 发送 GET 请求")

# 替换成你想查询的 GitHub 用户名
username = "octocat"

# 拼接 URL：https://api.github.com/users/octocat
url = f"{GITHUB_API}/users/{username}"

print(f"请求地址: {url}")
print(f"请求头  : {HEADERS}")

# 发送 GET 请求，headers 参数传入自定义请求头
response = requests.get(url, headers=HEADERS)

show_status(response)

# ─────────────────────────────────────────
# 第 2 步：解析 JSON 响应
# ─────────────────────────────────────────
section("第 2 步：解析返回的 JSON 数据")

# response.json() 将响应体解析为 Python dict
user = response.json()

show_json(user, "用户完整信息（部分字段）")

# ─────────────────────────────────────────
# 第 3 步：提取并打印关键字段
# ─────────────────────────────────────────
section("第 3 步：提取关键字段")

# 用户基本信息
print(f"用户名    : {user.get('login', '未知')}")
print(f"昵称      : {user.get('name') or '（未设置）'}")
print(f"头像地址  : {user.get('avatar_url', '未知')}")
print(f"主页      : {user.get('html_url', '未知')}")

# 数据类字段（数字）
print(f"公开仓库数: {user.get('public_repos', 0)} 个")
print(f"Followers : {user.get('followers', 0)} 人")
print(f"Following : {user.get('following', 0)} 人")

# ─────────────────────────────────────────
# 第 4 步：理解返回数据结构
# ─────────────────────────────────────────
section("第 4 步：观察返回数据的所有 Key")

# 打印 JSON 所有顶层字段名，方便了解数据结构
print("返回 JSON 的所有字段名：")
for key in user.keys():
    value = user[key]
    # 只打印简短值，长内容用省略号
    if isinstance(value, (str, int, float, bool, type(None))):
        display = str(value)[:60]
    else:
        display = type(value).__name__
    print(f"  {key:25s} → {display}")

print("\n✅ 本节完成！你已学会向 GitHub API 发送基础 GET 请求并解析用户信息。")

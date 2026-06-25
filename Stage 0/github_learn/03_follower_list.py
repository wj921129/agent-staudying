"""
03 - 获取并打印 Follower 列表
==============================
学习要点：
  1. 调用 /users/{username}/followers 接口获取粉丝列表
  2. 遍历返回列表，提取每个 follower 的关键信息
  3. 格式化打印表格

API 文档：https://docs.github.com/rest/users/followers#list-followers-of-a-user
"""

import requests
from utils import GITHUB_API, HEADERS, section, show_status

# 替换成你想查询的 GitHub 用户名
username = "octocat"

# ─────────────────────────────────────────
# 第 1 步：请求 followers 列表（第一页）
# ─────────────────────────────────────────
section("第 1 步：获取 followers 列表")

url = f"{GITHUB_API}/users/{username}/followers"

# per_page=10  为了演示方便，只取前 10 条
params = {"per_page": 10}

print(f"请求地址: {url}")
print(f"查询参数: {params}")

response = requests.get(url, headers=HEADERS, params=params)
show_status(response)

# ─────────────────────────────────────────
# 第 2 步：解析返回的列表数据
# ─────────────────────────────────────────
section("第 2 步：理解返回的数据结构")

followers = response.json()

# 返回的是一个 list[dict]，每个 dict 是一个 follower 的简要信息
print(f"返回类型: {type(followers).__name__}，共 {len(followers)} 条")

if followers:
    first = followers[0]
    print("\n第一个 follower 包含的字段：")
    for key in first.keys():
        value = first[key]
        display = str(value)[:50] if not isinstance(value, dict) else "dict"
        print(f"  {key:20s} → {display}")

# ─────────────────────────────────────────
# 第 3 步：格式化打印 follower 表格
# ─────────────────────────────────────────
section("第 3 步：格式化打印 follower 列表")

print(f"\n{'序号':>4}  {'用户名':<20} {'个人主页'}")
print("-" * 70)

for i, follower in enumerate(followers, 1):
    login = follower.get("login", "未知")
    html_url = follower.get("html_url", "")
    print(f"{i:4}  {login:<20} {html_url}")

# ─────────────────────────────────────────
# 第 4 步：提取更多有用信息
# ─────────────────────────────────────────
section("第 4 步：汇总统计")

# 统计字段说明
avatar_count = sum(1 for f in followers if f.get("avatar_url"))
site_admin_count = sum(1 for f in followers if f.get("site_admin"))

print(f"\n本次获取 : {len(followers)} 个 follower")
print(f"有头像的 : {avatar_count} 人")
print(f"站点管理员: {site_admin_count} 人")

print("\n💡 提示：这只是第一页数据，完整列表需要处理分页（见 05 节）。")
print("\n✅ 本节完成！你已学会获取并格式化打印 follower 列表。")

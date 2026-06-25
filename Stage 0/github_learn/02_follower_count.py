"""
02 - 获取并打印 Follower 数量
==============================
学习要点：
  1. 从用户资料接口直接读取 followers 字段（数量）
  2. 调用 followers 列表接口，实际统计条数
  3. 理解两种方式的差异与适用场景

API 文档：
  用户资料：https://docs.github.com/rest/users/users#get-a-user
  粉丝列表：https://docs.github.com/rest/users/followers#list-followers-of-a-user
"""

import requests
from utils import GITHUB_API, HEADERS, section, show_status

# 替换成你想查询的 GitHub 用户名
username = "octocat"

# ─────────────────────────────────────────
# 方式一：从用户资料接口读取 followers 字段（最快）
# ─────────────────────────────────────────
section("方式一：从用户资料接口直接读取 followers 数量")

url = f"{GITHUB_API}/users/{username}"
response = requests.get(url, headers=HEADERS)
show_status(response)

user = response.json()

# followers 字段是 GitHub 预先计算好的数字，一次请求即可获得
follower_count = user.get("followers", 0)
following_count = user.get("following", 0)

print(f"\n👤 用户: {username}")
print(f"   Followers : {follower_count} 人")
print(f"   Following : {following_count} 人")
print(f"   比值      : 1 : {following_count / max(follower_count, 1):.2f}")

# ─────────────────────────────────────────
# 方式二：调用 followers 列表接口，统计返回条数
# ─────────────────────────────────────────
section("方式二：通过 followers 列表接口统计（第一页）")

followers_url = f"{GITHUB_API}/users/{username}/followers"

# per_page 参数：每页返回条数（默认 30，最大 100）
response = requests.get(followers_url, headers=HEADERS, params={"per_page": 100})
show_status(response)

followers_page = response.json()

print(f"\n本页返回 : {len(followers_page)} 条")
print("⚠️  注意：列表接口默认每页 30 条，最多 100 条。")
print("   如果用户 followers 超过 100 人，需要翻页才能获取全部（见 05 节）。")

# ─────────────────────────────────────────
# 两种方式的对比总结
# ─────────────────────────────────────────
section("对比总结")

print("""
┌─────────────────────┬─────────────────────┬──────────────────────┐
│ 方式                │ 请求次数            │ 适用场景             │
├─────────────────────┼─────────────────────┼──────────────────────┤
│ 用户资料接口        │ 1 次                │ 只需要数量           │
│ /users/{name}       │                     │ 快速、节省配额       │
├─────────────────────┼─────────────────────┼──────────────────────┤
│ 粉丝列表接口        │ 可能多次（分页）    │ 需要知道具体是谁     │
│ /users/{name}/      │                     │ 需要遍历粉丝详情     │
│   followers         │                     │                      │
└─────────────────────┴─────────────────────┴──────────────────────┘

💡 结论：只需要 follower 数量 → 用方式一（更快、更省配额）
""")

print("✅ 本节完成！你已掌握两种获取 follower 数量的方式。")

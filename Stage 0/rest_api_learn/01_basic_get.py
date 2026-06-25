"""
01 - 基础 GET 请求
==================
学习要点：
  1. requests.get() 发送 GET 请求
  2. response.json() 解析 JSON
  3. 传递 URL 查询参数 (params)
  4. 读取响应头 / 状态码
"""

import requests
from utils import section, show_json, show_status

BASE_URL = "https://jsonplaceholder.typicode.com"

# ─────────────────────────────────────────
# 示例 1：最简单的 GET 请求
# ─────────────────────────────────────────
section("示例 1：GET 获取单条数据")

response = requests.get(f"{BASE_URL}/posts/1")

show_status(response)          # 查看状态码、URL
post = response.json()         # 解析 JSON → dict
show_json(post, "文章详情")

print(f"\n标题: {post['title']}")
print(f"内容: {post['body'][:60]}...")

# ─────────────────────────────────────────
# 示例 2：获取列表 + 查询参数
# ─────────────────────────────────────────
section("示例 2：GET 获取列表 + params 查询参数")

# params 会自动拼接成 ?userId=1&_limit=3
params = {"userId": 1, "_limit": 3}
response = requests.get(f"{BASE_URL}/posts", params=params)

show_status(response)
print(f"实际请求 URL: {response.url}")

posts = response.json()        # 解析 JSON → list[dict]
print(f"\n共返回 {len(posts)} 条文章：")
for i, p in enumerate(posts, 1):
    print(f"  [{i}] {p['title']}")

# ─────────────────────────────────────────
# 示例 3：读取响应头信息
# ─────────────────────────────────────────
section("示例 3：读取响应头")

response = requests.get(f"{BASE_URL}/users/1")

print(f"Content-Type   : {response.headers['Content-Type']}")
print(f"Cache-Control  : {response.headers.get('Cache-Control', '无')}")
print(f"字符编码       : {response.encoding}")

user = response.json()
show_json(user, "用户信息")

# ─────────────────────────────────────────
# 示例 4：解析嵌套 JSON
# ─────────────────────────────────────────
section("示例 4：解析嵌套 JSON 结构")

response = requests.get(f"{BASE_URL}/users/1")
user = response.json()

# 嵌套字段访问
print(f"用户名  : {user['username']}")
print(f"邮箱    : {user['email']}")
print(f"城市    : {user['address']['city']}")
print(f"经度    : {user['address']['geo']['lng']}")
print(f"公司    : {user['company']['name']}")

print("\n✅ 本节完成！基础 GET 请求 + JSON 解析已掌握。")

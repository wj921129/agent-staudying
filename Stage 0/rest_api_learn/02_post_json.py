"""
02 - POST 请求 + JSON 解析
===========================
学习要点：
  1. requests.post() 发送 JSON body
  2. json 参数 vs data 参数的区别
  3. 解析服务端返回的 JSON
  4. PUT / PATCH / DELETE 方法
"""

import requests
from utils import section, show_json, show_status

BASE_URL = "https://jsonplaceholder.typicode.com"

# ─────────────────────────────────────────
# 示例 1：用 json= 发送 POST 请求（推荐）
# ─────────────────────────────────────────
section("示例 1：POST + json= 参数（自动序列化）")

payload = {
    "title": "我的新文章",
    "body": "这是一篇关于 Python REST API 的学习笔记。",
    "userId": 1,
}

# json= 会自动：
#   1. 把 dict 序列化为 JSON 字符串
#   2. 设置 Content-Type: application/json
response = requests.post(f"{BASE_URL}/posts", json=payload)

show_status(response)
result = response.json()
show_json(result, "创建成功 - 服务端返回")

print(f"\n新文章 ID: {result['id']}")   # jsonplaceholder 会返回 id: 101

# ─────────────────────────────────────────
# 示例 2：用 data= 发送（需手动设置 header）
# ─────────────────────────────────────────
section("示例 2：POST + data= 参数（手动序列化）")

import json

payload_str = json.dumps(payload, ensure_ascii=False)
headers = {"Content-Type": "application/json; charset=utf-8"}

response = requests.post(
    f"{BASE_URL}/posts",
    data=payload_str,           # 传字符串，需要手动 json.dumps
    headers=headers,            # 需要手动设置 Content-Type
)

show_status(response)
show_json(response.json(), "创建成功 - data= 方式")

print("\n💡 json= 和 data= 的区别：")
print("   json=dict  → requests 自动序列化 + 自动设 Content-Type")
print("   data=str   → 需要自己 json.dumps + 自己设 header")
print("   推荐优先使用 json= 参数，更简洁不易出错。")

# ─────────────────────────────────────────
# 示例 3：POST 表单数据（非 JSON）
# ─────────────────────────────────────────
section("示例 3：POST 表单数据（data=dict）")

# data=dict 时会以 form-urlencoded 格式发送（Content-Type: application/x-www-form-urlencoded）
form_data = {
    "username": "testuser",
    "password": "secret123",
}

response = requests.post("https://httpbin.org/post", data=form_data)

show_status(response)
if response.ok:
    resp = response.json()
    print(f"\n服务端收到的 form 数据: {resp['form']}")
    print(f"Content-Type: {resp['headers']['Content-Type']}")
else:
    print(f"httpbin.org 暂时不可用（{response.status_code}），跳过表单展示。")

# ─────────────────────────────────────────
# 示例 4：PUT / PATCH / DELETE
# ─────────────────────────────────────────
section("示例 4：PUT / PATCH / DELETE 方法")

# PUT - 完整替换
put_data = {"id": 1, "title": "更新后的标题", "body": "更新后的内容", "userId": 1}
response = requests.put(f"{BASE_URL}/posts/1", json=put_data)
print(f"PUT  /posts/1  → 状态码: {response.status_code}")

# PATCH - 部分更新
patch_data = {"title": "只改标题"}
response = requests.patch(f"{BASE_URL}/posts/1", json=patch_data)
print(f"PATCH /posts/1 → 状态码: {response.status_code}")

# DELETE - 删除
response = requests.delete(f"{BASE_URL}/posts/1")
print(f"DELETE /posts/1 → 状态码: {response.status_code}")

print("\n✅ 本节完成！POST / PUT / PATCH / DELETE 已掌握。")

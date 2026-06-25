"""
06 - 进阶技巧
=============
学习要点：
  1. 超时配置（connect + read 分离）
  2. 指数退避重试（Exponential Backoff）
  3. 分页处理（自动翻页获取全部数据）
  4. 文件上传
  5. 流式下载大文件
"""

import time
import requests
from utils import section, show_json

HTTPBIN = "https://httpbin.org"
JSONPLACEHOLDER = "https://jsonplaceholder.typicode.com"

# ─────────────────────────────────────────
# 示例 1：超时配置（connect + read 分离）
# ─────────────────────────────────────────
section("示例 1：超时配置")

def check_httpbin(resp):
    """httpbin 服务不可用时友好提示"""
    if not resp.ok and resp.status_code != 500:  # 500 是本节故意触发的
        print(f"  ⚠ httpbin.org 暂时不可用（{resp.status_code}），跳过。")
        return False
    return True


# timeout 可以是单个值（connect + read 共用）
r = requests.get(f"{HTTPBIN}/get", timeout=5)
if check_httpbin(r):
    print(f"单值超时 5s → 状态码: {r.status_code}")

# 也可以用元组 (connect_timeout, read_timeout) 分别设置
# connect: 建立连接的超时
# read:    等待响应数据的超时
r = requests.get(f"{HTTPBIN}/get", timeout=(3, 10))
if check_httpbin(r):
    print(f"分离超时 (连接3s, 读取10s) → 状态码: {r.status_code}")

print("\n💡 生产环境务必设置 timeout，否则请求可能永远阻塞！")
print("   建议值：connect=3~5s, read=10~30s")

# ─────────────────────────────────────────
# 示例 2：指数退避重试（Exponential Backoff）
# ─────────────────────────────────────────
section("示例 2：指数退避重试")


def request_with_backoff(
    method: str,
    url: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
    timeout: tuple = (5, 10),
    **kwargs,
) -> requests.Response:
    """
    带指数退避的请求。
    每次失败后等待时间翻倍：1s → 2s → 4s → ...
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            response = requests.request(
                method, url, timeout=timeout, **kwargs
            )
            response.raise_for_status()
            print(f"  ✓ 第 {attempt + 1} 次尝试成功")
            return response

        except (requests.HTTPError, requests.ConnectionError,
                requests.Timeout) as e:
            last_exception = e
            delay = base_delay * (2 ** attempt)   # 1s, 2s, 4s
            print(f"  ✗ 第 {attempt + 1} 次失败: {type(e).__name__}")
            if attempt < max_retries - 1:
                print(f"    等待 {delay}s 后重试...")
                time.sleep(delay)

    raise RuntimeError(f"重试 {max_retries} 次后仍失败: {last_exception}")


# 成功情况
print("测试 A - 正常请求：")
try:
    r = request_with_backoff("GET", f"{HTTPBIN}/get")
    print(f"  状态码: {r.status_code}")
except RuntimeError as e:
    print(f"  失败: {e}")

# 失败情况（500 会触发重试）
print("\n测试 B - 500 错误（触发退避重试）：")
try:
    r = request_with_backoff("GET", f"{HTTPBIN}/status/500", max_retries=3, base_delay=0.5)
except RuntimeError as e:
    print(f"  最终失败: {e}")

# ─────────────────────────────────────────
# 示例 3：分页处理（自动翻页）
# ─────────────────────────────────────────
section("示例 3：分页处理 - 自动获取全部数据")


def fetch_all_paginated(base_url: str, per_page: int = 10) -> list:
    """
    自动翻页获取所有数据。
    适用于支持 _page / _limit 的 API（jsonplaceholder 风格）。

    分页策略因 API 而异，常见方式：
      1. ?page=1&per_page=10  （页码式）
      2. ?offset=0&limit=10   （偏移式）
      3. ?cursor=abc123       （游标式）
    """
    all_data = []
    page = 1

    while True:
        params = {"_page": page, "_limit": per_page}
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        items = response.json()
        if not items:            # 空列表说明已翻完
            break

        all_data.extend(items)
        print(f"  第 {page} 页: 获取 {len(items)} 条（累计 {len(all_data)} 条）")

        # 如果返回数量 < per_page，说明是最后一页
        if len(items) < per_page:
            break
        page += 1

    return all_data


print("获取 /comments 所有数据（每页 25 条）：")
all_comments = fetch_all_paginated(
    f"{JSONPLACEHOLDER}/comments",
    per_page=25,
)
print(f"\n总计获取: {len(all_comments)} 条评论")

# ─────────────────────────────────────────
# 示例 4：文件上传
# ─────────────────────────────────────────
section("示例 4：文件上传")

# 方式 A：上传文件（multipart/form-data）
# 模拟一个文件对象（无需真实文件）
file_content = b"Hello, this is a test file content!"
files = {
    "file": ("test.txt", file_content, "text/plain"),
}

response = requests.post(f"{HTTPBIN}/post", files=files)
if check_httpbin(response):
    resp = response.json()
    print(f"上传状态码: {response.status_code}")
    print(f"服务端收到的文件: {resp['files']}")
else:
    print(f"  ⚠ httpbin 不可用（{response.status_code}），上传展示跳过。")

# 方式 B：同时上传文件 + 表单数据
files_with_data = {
    "file": ("report.csv", b"id,name\n1,Alice\n2,Bob", "text/csv"),
}
form_fields = {
    "description": "月度报告",
    "author": "Python",
}

response = requests.post(
    f"{HTTPBIN}/post",
    files=files_with_data,
    data=form_fields,       # 额外的表单字段
)
if check_httpbin(response):
    resp = response.json()
    print(f"\n文件 + 表单上传：")
    print(f"  files : {resp['files']}")
    print(f"  form  : {resp['form']}")
else:
    print(f"  ⚠ httpbin 不可用，文件+表单上传跳过。")

# ─────────────────────────────────────────
# 示例 5：流式下载大文件
# ─────────────────────────────────────────
section("示例 5：流式下载（stream=True）")

# stream=True 不会立刻把整个响应加载到内存
# 适合下载大文件（视频、大型 CSV 等）
url = f"{HTTPBIN}/bytes/1024"   # 模拟 1KB 文件

try:
    response = requests.get(url, stream=True, timeout=10)
    response.raise_for_status()

    total_bytes = 0
    # 分块读取（每次 512 字节）
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            total_bytes += len(chunk)
            print(f"  读取 chunk: {len(chunk)} bytes（累计 {total_bytes} bytes）")

    print(f"\n下载完成！总计: {total_bytes} bytes")
except requests.RequestException as e:
    print(f"  ⚠ httpbin.org 不可用（{e}），流式下载跳过。")

print("""
💡 stream=True 的最佳实践：
   with requests.get(url, stream=True) as r:
       r.raise_for_status()
       with open("large_file.zip", "wb") as f:
           for chunk in r.iter_content(chunk_size=8192):
               f.write(chunk)
""")

print("✅ 本节完成！进阶技巧已全部掌握。")
print("\n🎉 恭喜！REST API 全套学习完成（01~06），你已具备：")
print("   ✓ GET / POST / PUT / PATCH / DELETE")
print("   ✓ JSON 解析（含嵌套结构）")
print("   ✓ Bearer Token / API Key / Basic Auth")
print("   ✓ Session 持久化 + API 客户端封装")
print("   ✓ 错误处理 + 指数退避重试")
print("   ✓ 分页 / 文件上传 / 流式下载")

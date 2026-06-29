"""
05 - 分页处理：获取全部 Followers
==================================
学习要点：
  1. GitHub API 分页机制（page + per_page 参数）
  2. 通过 Link 响应头判断是否有下一页
  3. 使用 while 循环逐页获取全部数据
  4. 封装一个完整的「获取全部 followers」函数

API 文档：https://docs.github.com/rest/overview/resources-in-the-rest-api#pagination
"""

import requests
from utils import GITHUB_API, HEADERS, section, show_status

# 替换成你想查询的 GitHub 用户名
username = "octocat"

# ─────────────────────────────────────────
# 第 1 步：理解 GitHub 的分页参数
# ─────────────────────────────────────────
section("第 1 步：GitHub API 分页参数说明")

print("""
  GitHub 列表接口支持两个分页参数：
    per_page  每页条数（默认 30，最大 100）
    page      页码（从 1 开始）

  示例：
    ?per_page=100&page=1  → 第 1 页，每页 100 条
    ?per_page=100&page=2  → 第 2 页，每页 100 条

  响应头 Link 字段会告诉你是否有下一页：
    Link: <https://...?page=2>; rel="next",
          <https://...?page=5>; rel="last"
""")

# ─────────────────────────────────────────
# 第 2 步：手动请求两页数据，观察 Link 头
# ─────────────────────────────────────────
section("第 2 步：手动翻页，观察 Link 响应头")

url = f"{GITHUB_API}/users/{username}/followers"

# 第一页（每页 5 条，方便演示）
response = requests.get(url, headers=HEADERS, params={"per_page": 5, "page": 1})
show_status(response)
print(f"第 1 页返回: {len(response.json())} 条")

# Link 头包含分页链接
link_header = response.headers.get("Link", "无")
print(f"Link 响应头: {link_header[:120]}...")

# 第二页
response2 = requests.get(url, headers=HEADERS, params={"per_page": 5, "page": 2})
print(f"第 2 页返回: {len(response2.json())} 条")

# ─────────────────────────────────────────
# 第 3 步：封装分页工具函数
# ─────────────────────────────────────────
section("第 3 步：封装 get_all_followers() 函数")

import re


def get_next_url(link_header: str) -> str | None:
    """
    解析 Link 响应头，提取 rel="next" 的 URL。
    如果没有下一页，返回 None。

    Link 头格式示例：
      <https://api.github.com/...?page=2>; rel="next",
      <https://api.github.com/...?page=5>; rel="last"
    """
    if not link_header:
        return None

    # 用正则匹配 rel="next" 对应的 URL
    match = re.search(r'<([^>]+)>;\s*rel="next"', link_header)
    return match.group(1) if match else None


def get_all_followers(username: str, max_pages: int = 5) -> list:
    """
    逐页获取指定用户的全部 followers。
    max_pages: 最多翻几页（防止无限请求，保护配额）
    """
    all_followers = []
    page = 1

    url = f"{GITHUB_API}/users/{username}/followers"
    params = {"per_page": 100, "page": page}

    while page <= max_pages:
        print(f"  正在获取第 {page} 页...", end=" ")
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)

        if response.status_code != 200:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            break

        page_data = response.json()
        print(f"返回 {len(page_data)} 条")
        all_followers.extend(page_data)

        # 检查是否有下一页
        next_url = get_next_url(response.headers.get("Link", ""))
        if not next_url or len(page_data) == 0:
            print("  ✅ 已到最后一页")
            break

        # 更新参数，准备请求下一页
        page += 1
        params["page"] = page

    return all_followers


# ─────────────────────────────────────────
# 第 4 步：调用函数，打印全部 followers
# ─────────────────────────────────────────
section("第 4 步：获取并打印全部 followers")

print(f"\n开始获取 '{username}' 的 followers（最多 5 页 = 500 条）：")
all_followers = get_all_followers(username, max_pages=5)

print(f"\n总计获取: {len(all_followers)} 个 followers")

# 打印前 15 个
print(f"\n前 15 个 follower：")
print(f"{'序号':>4}  {'用户名':<25} {'主页'}")
print("-" * 70)
for i, f in enumerate(all_followers[:15], 1):
    login = f.get("login", "未知")
    html_url = f.get("html_url", "")
    print(f"{i:4}  {login:<25} {html_url}")

if len(all_followers) > 15:
    print(f"  ...（省略剩余 {len(all_followers) - 15} 条）")

# ─────────────────────────────────────────
# 总结
# ─────────────────────────────────────────
section("本节小结")

print("""
  1. GitHub 列表接口默认每页 30 条，最多 100 条
  2. 通过 Link 响应头的 rel="next" 判断是否有下一页
  3. 用 while 循环 + page 参数逐页累积数据
  4. 务必设置 max_pages 上限，防止配额耗尽

  💡 进阶技巧：
     - 使用 Personal Access Token 提升配额（5000 次/小时）
     - 使用 time.sleep() 控制请求频率，避免触发限流
""")

print("✅ 全部完成！你已掌握 GitHub API 的完整分页处理方式。")

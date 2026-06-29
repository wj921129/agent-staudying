"""
GitHub API 学习 —— 公共工具函数
"""
import json
from pprint import pprint


# GitHub API 基础地址
GITHUB_API = "https://api.github.com"

# 公共请求头：GitHub API 推荐使用 v3 版本
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Python-GitHub-Learner",
}


def section(title: str):
    """打印分节标题"""
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print(f"{'=' * 50}")


def show_json(data, title: str = "响应 JSON"):
    """美化打印 JSON 数据"""
    print(f"\n--- {title} ---")
    pprint(data, sort_dicts=False)


def show_status(response):
    """打印响应状态信息"""
    print(f"状态码  : {response.status_code}")
    print(f"请求 URL: {response.url}")
    remaining = response.headers.get("X-RateLimit-Remaining", "未知")
    print(f"剩余配额: {remaining} 次")

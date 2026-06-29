"""
公共工具函数 —— 被所有 demo 文件引用
"""
import json
from pprint import pprint


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
    print(f"状态码: {response.status_code}")
    print(f"请求URL: {response.url}")
    print(f"响应头 Content-Type: {response.headers.get('Content-Type', 'N/A')}")

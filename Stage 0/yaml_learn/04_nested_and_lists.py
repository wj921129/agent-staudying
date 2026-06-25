"""
04_nested_and_lists.py
YAML 中的嵌套字典与列表

学习目标：
1. 学会写入/读取带嵌套结构的配置
2. 学会处理列表（数组）
3. 理解 YAML 缩进与 Python 数据结构之间的对应关系
"""

import yaml
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "nested_config.yaml"

# 第一步：构造一个包含嵌套结构和列表的配置
config = {
    "app_name": "First Demo",
    "debug": False,
    "server": {
        "host": "0.0.0.0",
        "port": 8080,
        "ssl": {
            "enabled": True,
            "cert": "/path/to/cert.pem",
            "key": "/path/to/key.pem",
        },
    },
    "database": {
        "host": "localhost",
        "port": 3306,
        "name": "first_demo_db",
        "pool_size": 10,
    },
    "features": ["auth", "logging", "cache"],
    "users": [
        {"name": "admin", "role": "superuser"},
        {"name": "guest", "role": "readonly"},
    ],
}

print("原始 Python 数据结构：")
print(config)
print()

# 第二步：写入 YAML
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    yaml.safe_dump(
        config,
        f,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,  # 这里保留原始顺序，方便观察
    )

print(f"✅ 嵌套配置已写入：{OUTPUT_FILE}")
print()

# 第三步：展示 YAML 内容
print("--- YAML 内容 ---")
print(OUTPUT_FILE.read_text(encoding="utf-8"))

# 第四步：读取并访问嵌套数据
with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
    loaded = yaml.safe_load(f)

print("--- 读取后访问嵌套数据 ---")
print(f"服务器地址：{loaded['server']['host']}")
print(f"SSL 是否启用：{loaded['server']['ssl']['enabled']}")
print(f"数据库名：{loaded['database']['name']}")
print(f"功能列表：{loaded['features']}")
print(f"第一个用户：{loaded['users'][0]}")
print(f"第二个用户的角色：{loaded['users'][1]['role']}")

# 第五步：遍历列表
print()
print("--- 遍历用户列表 ---")
for user in loaded["users"]:
    print(f"  - {user['name']}：{user['role']}")

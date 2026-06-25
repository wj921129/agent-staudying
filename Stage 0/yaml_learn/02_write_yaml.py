"""
02_write_yaml.py
Python 写入 YAML 配置文件

学习目标：
1. 用 yaml.safe_dump() 把 Python 字典写入 .yaml 文件
2. 掌握 sort_keys、allow_unicode、default_flow_style 等常用参数
3. 理解文件写入的流程
"""

import yaml
from pathlib import Path

# 定义输出路径（放在本文件同级目录下的 output 文件夹中）
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "basic_config.yaml"

# 第一步：准备要写入的 Python 字典
config = {
    "app_name": "First Demo",
    "version": "1.0.0",
    "debug": True,
    "author": "你的名字",
    "port": 8080,
}

print("原始 Python 字典：")
print(config)
print()

# 第二步：写入 YAML 文件
# safe_dump() 是最常用的写入方法，安全且支持中文
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    yaml.safe_dump(
        config,
        f,
        allow_unicode=True,        # 允许中文正常显示，不会转义
        default_flow_style=False,  # 使用块样式（更易读），不用内联样式
        sort_keys=True,            # 按键排序输出
    )

print(f"✅ 配置已写入文件：{OUTPUT_FILE}")
print()

# 第三步：读取文件内容展示给用户
print("--- 写入的 YAML 内容 ---")
print(OUTPUT_FILE.read_text(encoding="utf-8"))

# 补充说明：default_flow_style=False 与 True 的区别
print("--- 对比：default_flow_style=True 的效果 ---")
inline = yaml.safe_dump(config, allow_unicode=True, default_flow_style=True)
print(inline)
print("提示：False 适合配置文件，True 适合压缩传输。")

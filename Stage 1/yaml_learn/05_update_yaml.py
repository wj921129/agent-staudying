"""
05_update_yaml.py
读取 YAML → 修改内容 → 写回 YAML

学习目标：
1. 掌握“读-改-写”的完整流程
2. 注意写回时会丢失原文件中的注释（这是 PyYAML 的局限）
3. 了解如果需要保留注释，可以使用 ruamel.yaml 库
"""

import yaml
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "updatable_config.yaml"

# 第一步：创建初始配置文件
initial_content = """
# 注意：这是初始配置
app_name: First Demo
version: 1.0.0
debug: false
port: 8080
features:
  - auth
  - logging
"""
OUTPUT_FILE.write_text(initial_content, encoding="utf-8")
print(f"✅ 初始配置已写入：{OUTPUT_FILE}")
print()
print("--- 修改前 ---")
print(OUTPUT_FILE.read_text(encoding="utf-8"))

# 第二步：读取配置
with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 第三步：修改配置
config["version"] = "1.1.0"
config["debug"] = True
config["port"] = 9000
config["features"].append("cache")
config.setdefault("new_feature", "hello yaml")

print("--- 修改后的 Python 对象 ---")
print(config)
print()

# 第四步：写回文件
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    yaml.safe_dump(
        config,
        f,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )

print("--- 修改后的 YAML 文件 ---")
print(OUTPUT_FILE.read_text(encoding="utf-8"))
print()
print("⚠️ 提示：用 yaml.safe_dump 写回后，原 YAML 里的注释会丢失。")
print("如果需要保留注释，可以使用 ruamel.yaml 库：pip install ruamel.yaml")

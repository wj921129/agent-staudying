"""
03_read_yaml.py
Python 读取 YAML 配置文件

学习目标：
1. 用 yaml.safe_load() 读取 .yaml 文件
2. 处理文件不存在的情况
3. 读取后用字典方式访问配置项
"""

import yaml
from pathlib import Path

# 本文件会创建一个示例 YAML，然后再读取它，保证单独运行也能成功
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
SAMPLE_FILE = OUTPUT_DIR / "app_config.yaml"

# 第一步：先准备一个示例 YAML 文件（模拟已有的配置文件）
sample_content = """
# 应用配置文件
app_name: First Demo
version: 1.0.0
debug: true
port: 8080
"""
SAMPLE_FILE.write_text(sample_content, encoding="utf-8")
print(f"✅ 示例配置文件已准备：{SAMPLE_FILE}")
print()

# 第二步：读取 YAML 文件
# 推荐做法：先判断文件是否存在，避免直接报错
if not SAMPLE_FILE.exists():
    print(f"❌ 文件不存在：{SAMPLE_FILE}")
else:
    with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    print("--- 读取结果 ---")
    print("类型：", type(config))
    print("内容：", config)
    print()

    # 第三步：访问具体配置项
    print("--- 访问配置项 ---")
    print(f"应用名称：{config['app_name']}")
    print(f"版本号：{config['version']}")
    print(f"调试模式：{config['debug']}")
    print(f"端口：{config['port']}")
    print()

    # 第四步：安全访问（防止键不存在报错）
    print("--- 安全访问（get 方法）---")
    timeout = config.get("timeout", 30)
    print(f"timeout 配置：{timeout}")
    print("提示：用 get() 可以设置默认值，键不存在时不会报错。")

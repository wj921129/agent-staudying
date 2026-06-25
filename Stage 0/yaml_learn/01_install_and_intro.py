"""
01_install_and_intro.py
Python 读写 YAML 配置文件：安装检查与 YAML 简介

学习目标：
1. 确认 PyYAML 库是否已安装
2. 了解 YAML 的基本语法特点
3. 知道为什么配置文件常用 YAML
"""

# 第一步：检查 PyYAML 是否可用
try:
    import yaml
    print("✅ PyYAML 已安装，版本：", yaml.__version__)
except ImportError:
    print("❌ PyYAML 未安装，请在终端运行以下命令安装：")
    print("   pip install pyyaml")
    print("或在 PyCharm 中：File -> Settings -> Project -> Python Interpreter -> + -> PyYAML")
    raise

print()
print("--- YAML 简介 ---")
print("YAML（YAML Ain't Markup Language）是一种人类可读的数据序列化格式。")
print("它比 JSON 更简洁，支持注释，非常适合做配置文件。")
print()
print("基本规则：")
print("- 使用缩进表示层级（推荐 2 个空格，不要用 Tab）")
print("- 键值对用冒号 + 空格分隔：key: value")
print("- 列表用 - 开头")
print("- 可以用 # 写注释")
print()
print("示例 YAML 内容：")
sample_yaml = """
# 这是一个注释
app_name: First Demo
version: 1.0
debug: true
ports:
  - 8080
  - 8081
database:
  host: localhost
  port: 3306
"""
print(sample_yaml)

# 验证上面的字符串可以解析
parsed = yaml.safe_load(sample_yaml)
print("解析后的 Python 对象：")
print(parsed)

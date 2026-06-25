"""
06_safe_vs_load.py
为什么推荐使用 yaml.safe_load()

学习目标：
1. 理解 yaml.load() 和 yaml.safe_load() 的区别
2. 知道 safe_load 只能识别基本数据类型，更安全
3. 养成默认使用 safe_load / safe_dump 的习惯
"""

import yaml

print("--- yaml.load() 与 yaml.safe_load() 的区别 ---")
print()
print("yaml.load()：")
print("- 默认会解析 YAML 里的所有 Python 对象标签（!!python/object 等）")
print("- 如果 YAML 来源不可信，可能执行任意代码，存在安全风险")
print("- 新版 PyYAML 要求必须指定 Loader，否则报错")
print()
print("yaml.safe_load()：")
print("- 只解析标准 YAML 数据类型：dict、list、str、int、float、bool、None")
print("- 不会执行任意 Python 对象")
print("- 读取配置文件时首选")
print()

# 正常 YAML
normal_yaml = """
app_name: First Demo
users:
  - admin
  - guest
port: 8080
"""

print("--- 用 safe_load 解析正常 YAML ---")
result = yaml.safe_load(normal_yaml)
print(result)
print()

# 包含 Python 对象标签的 YAML（仅演示，不要实际使用）
# 注意：这段代码只是解释安全风险，不会真正执行危险操作
unsafe_yaml = """
!!python/object/apply:os.getuid []
"""

print("--- 演示：不安全 YAML 在 safe_load 下会被拒绝 ---")
try:
    bad = yaml.safe_load(unsafe_yaml)
    print("解析结果：", bad)
except yaml.YAMLError as e:
    print(f"✅ safe_load 成功拦截：{e}")

print()
print("--- 正确写法总结 ---")
print("读取：yaml.safe_load(file)")
print("写入：yaml.safe_dump(data, file)")
print("这两个方法足够应付 99% 的配置文件场景。")

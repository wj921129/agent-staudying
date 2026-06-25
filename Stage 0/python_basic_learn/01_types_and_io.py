# ============ 01 数据类型与输入输出 ============
# 知识点：基本输出、数据类型、type()、input()、math模块

# --- 1. 基本输出与字符串拼接 ---
name = "lilei"
print("hello world : " + name)

# --- 2. math 模块：向上取整与向下取整 ---
import math

a = -3.2
b = -2.2
print(f"a * b = {a * b}")
print(f"math.ceil(a * b) = {math.ceil(a * b)}")    # 向上取整
print(f"math.floor(a * b) = {math.floor(a * b)}")  # 向下取整

# --- 3. 数据类型一览 ---
# Python 常见基础类型：int, float, str, bool, None
a = 1          # int 整数
b = 2.2        # float 浮点数
c = "123"      # str 字符串
d = False      # bool 布尔值
n = None       # NoneType 空值

print(type(a))       # <class 'int'>
print(type(b))       # <class 'float'>
print(type(c))       # <class 'str'>
print(type(d))       # <class 'bool'>
print(type(n))       # <class 'NoneType'>
print(type(a + b))   # int + float → float

# 字符串索引访问
print(f"c[0] = {c[0]}")  # 取第一个字符

# --- 4. input 输入（需要用户交互） ---
# 注意：input() 返回的始终是 str 类型
hi = input("你好呀：")
print(hi + "，有什么能帮助你")

prompt = "请输入"
user_name = input(prompt + "您的名字：")
user_age = input(prompt + "您的年纪：")
print(f"你好 {user_name}，你 {user_age} 岁了")

# --- 5. statistics 模块 ---
import statistics

# median 取中位数
print(f"statistics.median([11, -2, 34]) = {statistics.median([11, -2, 34])}")

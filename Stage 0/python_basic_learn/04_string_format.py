# ============ 04 字符串格式化 ============
# 知识点：Python 7 种字符串拼接/格式化方式

name_arr = ["小明", "小红", "小白"]
msg_content = "今年{x}岁了"
age = 18

# --- 1. f-string（推荐，最直观） ---
# 在字符串前加 f，花括号内直接写变量或表达式
print(f"{name_arr[0]}今年都已经{age}岁了")

# --- 2. str.format() 命名占位符 ---
# 花括号内写名称，format() 用关键字传值
print("{name}今年都已经{age}岁了".format(name=name_arr[0], age=18))

# --- 3. str.format() 位置占位符 ---
# 花括号内写序号，format() 按位置传值
print("{0}今年都已经{1}岁了".format(name_arr[0], 18))

# --- 4. str.format() 省略序号 ---
# 花括号留空，按顺序填充
print("{}今年都已经{}岁了".format(name_arr[0], 18))

# --- 5. + 拼接（注意类型必须一致，需要手动转 str） ---
print(name_arr[0] + "今年都已经" + str(age) + "岁了")

# --- 6. % 格式化（老式写法，了解即可） ---
# %s = 字符串, %d = 整数
print("%s今年都已经%d岁了" % (name_arr[0], age))

# --- 7. join 拼接列表中的多个字符串 ---
# 只能拼接字符串列表，数字需先转 str
print("".join([name_arr[0], "今年都已经", str(age), "岁了"]))

# --- 补充：format 配合字典遍历 ---
print("\n--- format 配合字典遍历 ---")
name_dict = {"阿门": 18, "小红": 20, "米乐": 1.5}
print(f"米乐今年{name_dict['米乐']}岁了")

for key, value in name_dict.items():
    print(f"{key}今年{value:.2f}岁了")  # :.2f 保留两位小数

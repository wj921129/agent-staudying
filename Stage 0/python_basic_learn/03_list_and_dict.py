# ============ 03 列表与字典 ============
# 知识点：list 增删改查、dict CRUD、in 判断、遍历、列表推导式

# --- 1. 列表（list）基础操作 ---
name_list = ["李烈", "阿刁", "1"]
print(f"原始列表：{name_list}")

# 索引访问
print(f"name_list[0] = {name_list[0]}")

# 类型转换后运算
print(f"int(name_list[2]) + 2 = {int(name_list[2]) + 2}")

# 最大值、最小值（字符串按字典序比较）
print(f"max = {max(name_list)}, min = {min(name_list)}")

# 增：append
name_list.append("新增的")
print(f"append 后：{name_list}")

# 删：remove
name_list.remove(name_list[0])
print(f"remove 后：{name_list}")

# 改：索引赋值
name_list[0] = "修改的"
print(f"修改后：{name_list}")

# 排序：sorted 返回新列表
print(f"sorted：{sorted(name_list)}")

# --- 2. 列表推导式 ---
# [表达式 for 变量 in 可迭代对象 if 条件]
names = ['Bob', 'Tom', 'alice', 'Jerry', 'Wendy', 'Smith']
new_names = [name.upper() for name in names if len(name) > 3]
print(f"列表推导式结果：{new_names}")
# 等价于：
# new_names = []
# for name in names:
#     if len(name) > 3:
#         new_names.append(name.upper())

# 幂运算
print(f"2 ** 3 = {2 ** 3}")

# --- 3. 字典（dict）基础操作 ---
constant = {"小明": 20, "小红": 18}
print(f"原始字典：{constant}")

# 取值
print(f"constant['小明'] = {constant['小明']}")

# in 判断键是否存在
print(f"'小明' in constant → {'小明' in constant}")

if "小明" in constant:
    print("小明在字典中")

# 修改值
constant["小明"] += 1
print(f"修改后：{constant}")

# 字典常用方法
print(f"键的数量：{len(constant.keys())}")
print(f"小明 > 18？{constant['小明'] > 18}")

# --- 4. 字典遍历 ---
ages = {"小明": 20, "小红": 18, "小宝": 20}

# items() 同时遍历键和值
print("--- 遍历字典 ---")
for key, value in ages.items():
    print(f"{key}: {value}")

print("过了一年")
for key, value in ages.items():
    print(f"{key}: {value + 1}")

# --- 5. 字典配合 f-string 格式化 ---
name_dict = {"阿门": 18, "小红": 20, "米乐": 1.5}
print(f"米乐今年{name_dict['米乐']}岁了")

for key, value in name_dict.items():
    print(f"{key}今年{value:.2f}岁了")  # :.2f 保留两位小数

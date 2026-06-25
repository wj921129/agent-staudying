# ============ 02 条件判断与循环 ============
# 知识点：if/elif/else、for循环、while循环、range()

# --- 1. if / elif / else 条件判断 ---
# 模拟嵌套条件判断场景
mood_index = input("你今天的心情怎么样？\n")

if mood_index == "很好":
    print("那我就放心了")
    eat_status = input("你今天吃饭了没？\n")
    if eat_status == "吃了":
        print("那我就更放心了")
    else:
        print("那我就更担心了")
elif mood_index == "一般":
    eat_status = input("那你今天吃了没？\n")
    if eat_status == "吃了":
        print("吃了就好")
    else:
        print("那你赶快去吃饭")
else:
    print("那我就担心了")

# --- 2. for 循环 + range ---
# range(n) 生成 0 ~ n-1 的整数序列
for i in range(5):
    print(f"for循环第 {i} 次")

# 嵌套循环
for i in range(3):
    for j in range(3):
        print(f"i={i}, j={j}")

# --- 3. while 循环 ---
# 累加器：用户持续输入数字进行累加，输入 q 退出
a = input("请输入一个初始数字：\n")
print(f"您输入的数字是：{a}")
b = 0
c = a
while str(b) != "q":
    a = int(a) + int(b)
    if str(a) != str(c):
        print(f"结果是：{a}")
    b = input("请再输入一个相加的数字（输入 q 退出）：\n")

print("while 循环结束")

# ============ 05 基础函数 ============
# 知识点：函数定义、参数、返回值、sleep 模拟耗时

from time import sleep


# --- 1. 基本函数定义与调用 ---
def first_func(time, pName):
    """带耗时的函数：演示参数传递与返回值"""
    sleep(time)
    print('first func')
    sleep(time)
    print('second func')
    sleep(time)
    print(pName)
    return "func end"


# 调用函数并接收返回值
a = first_func(1, "lilei")
print(f"返回值：{a}")


# --- 2. 函数实战：BMI 计算 ---
def calculate_BMI(height, weight):
    """根据身高体重计算 BMI 并返回分类"""
    result = ""
    BMI = weight / (height ** 2)  # 标准 BMI 公式
    if BMI <= 18.5:
        result = "偏瘦"
    elif BMI <= 25:
        result = "正常"
    elif BMI <= 30:
        result = "偏胖"
    else:
        result = "肥胖"
    print(f"BMI = {BMI:.1f}，分类为：{result}")
    return result


# 调用 BMI 函数（身高 m，体重 kg）
result = calculate_BMI(1.75, 70)
print(f"最终结果：{result}")


# --- 3. 简单工具函数 ---
def print_hi(name):
    """打招呼函数"""
    print(f'Hi, {name}')


print_hi('Python')

# ============ 12 异常处理 ============
# 知识点：try/except/finally、assert、异常捕获策略


# --- 1. 基础 try / except / finally ---
# try 块中放可能出错的代码
# except 捕获异常
# finally 无论是否异常都会执行
try:
    a = 1
    result = str(a) + 2  # TypeError: 字符串不能与整数相加
except TypeError:
    print("TypeError：字符串不能与整数直接相加")
finally:
    print("finally：无论是否异常，这里都会执行")


# --- 2. 捕获不同类型的异常 ---
try:
    # 可以尝试修改下面的代码来触发不同异常
    num = int("abc")  # ValueError
except ValueError as e:
    print(f"ValueError：{e}")
except TypeError as e:
    print(f"TypeError：{e}")
except Exception as e:
    print(f"其他异常：{e}")
finally:
    print("finally：清理资源")


# --- 3. assert 断言 ---
# assert 用于调试，条件为 False 时抛出 AssertionError
try:
    a = "dff"
    assert a == "dff"       # 条件为 True，不报错
    print("a is dff")

    b = "fdd"
    assert b == "fdf"       # 条件为 False，抛出 AssertionError
except AssertionError:
    print("AssertionError：断言失败，b 不等于 'fdf'")
except Exception:
    print("anything is possible")
finally:
    print("finally：断言测试结束")


# --- 4. 自定义异常 ---
class BalanceError(Exception):
    """余额不足异常"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"余额不足：当前余额 {balance} 元，尝试取出 {amount} 元")


try:
    balance = 100
    amount = 200
    if amount > balance:
        raise BalanceError(balance, amount)
except BalanceError as e:
    print(f"捕获自定义异常：{e}")
    print(f"  当前余额：{e.balance}，尝试取出：{e.amount}")


# --- 5. 最佳实践总结 ---
# 1. 尽量捕获具体异常类型，不要裸 except
# 2. 用 finally 做资源清理（关闭文件、数据库连接等）
# 3. 用 assert 做开发阶段的调试检查
# 4. 自定义异常类继承 Exception，增加业务信息

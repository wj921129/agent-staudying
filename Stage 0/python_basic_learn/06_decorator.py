# ============ 06 装饰器 ============
# 知识点：装饰器原理、@语法糖、函数嵌套


# --- 1. 基础装饰器 ---
def my_decorator(func):
    """最简单的装饰器：在函数执行前后打印信息"""
    def wrapper():
        print("函数执行前")
        func()
        print("函数执行后")
    return wrapper


@my_decorator
def say_hello():
    print("Hello!")


# 调用被装饰的函数
say_hello()
# 等价于：say_hello = my_decorator(say_hello)


# --- 2. 带参数的装饰器 ---
def repeat(n):
    """装饰器工厂：让函数重复执行 n 次"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(n):
                print(f"--- 第 {i + 1} 次执行 ---")
                func(*args, **kwargs)
        return wrapper
    return decorator


@repeat(3)
def greet(name):
    print(f"你好，{name}！")


greet("Python")


# --- 3. 理解装饰器本质 ---
# 装饰器就是一个接收函数作为参数、返回新函数的高阶函数
# @decorator 语法糖等价于：func = decorator(func)

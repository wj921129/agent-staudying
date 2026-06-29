"""
【技巧1】覆盖 builtins.print —— 最简单的方式
===============================================
运行方式: python 14_override_print.py

原理:
  - Python 的 print 函数存放在 builtins 模块中
  - 只要修改 builtins.print，全局所有地方的 print 都会变
  - 只需在程序最开始 import 一次，后续文件不用再 import

优点: 简单直接，一行 import 生效
缺点: 修改了全局行为，第三方库的 print 也会受影响
"""
import builtins
import time

# 保存原始的 print
_original_print = builtins.print


# 定义新的 print，自动加上时间
def print(*args, **kwargs):
    """覆盖内置 print，自动加时间前缀"""
    timestamp = time.strftime("%H:%M:%S")
    # 把第一个参数加上时间前缀
    if args:
        first_arg = f"[{timestamp}] {args[0]}"
        _original_print(first_arg, *args[1:], **kwargs)
    else:
        _original_print(**kwargs)


# 替换 builtins.print
builtins.print = print


# ============================================================
# 下面直接用 print，不需要任何 import！
# ============================================================

if __name__ == "__main__":
    print("程序启动")
    time.sleep(1)
    print("1秒后...")

    # 正常传多个参数也支持
    print("多个参数:", "hello", "world")

    # end 参数也支持
    print("不换行测试: ", end="")
    print("紧接的内容")

    print("程序结束")

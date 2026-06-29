"""
【技巧2】包装 sys.stdout —— 更底层的方式
==========================================
运行方式: python 15_override_stdout.py

原理:
  - print 最终是写到 sys.stdout 这个对象
  - 把 sys.stdout 替换成自定义的包装类
  - 所有写到 stdout 的内容都会自动加时间

优点: 比覆盖 print 更彻底，连 logging 等输出也会受影响
缺点: 影响范围更大，需要小心处理换行逻辑
"""
import sys
import time


class TimestampStdout:
    """包装 sys.stdout，给每行输出加时间前缀"""

    def __init__(self, original_stdout):
        self._original = original_stdout
        self._line_start = True  # 标记是否是新行的开头

    def write(self, text):
        """拦截每次 write 调用"""
        if not text:
            return 0

        if self._line_start and text != "\n":
            # 新行的开头，加上时间前缀
            timestamp = time.strftime("%H:%M:%S")
            self._original.write(f"[{timestamp}] ")
            self._line_start = False

        self._original.write(text)

        # 如果以换行结尾，标记下一行是新的开始
        if text.endswith("\n"):
            self._line_start = True

        return len(text)

    def flush(self):
        """必须实现 flush 方法"""
        self._original.flush()

    def __getattr__(self, name):
        """代理其他所有属性到原始 stdout"""
        return getattr(self._original, name)


# 替换 sys.stdout
sys.stdout = TimestampStdout(sys.stdout)


# ============================================================
# 下面直接用 print，不需要任何 import！
# ============================================================

if __name__ == "__main__":
    print("程序启动")
    time.sleep(1)
    print("1秒后...")

    # 多个参数
    print("多个参数:", "hello", "world")

    # end 参数
    print("不换行: ", end="")
    print("紧接的内容")

    print("程序结束")

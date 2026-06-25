"""
【进阶6】异步迭代器 (async for)
===================================
运行方式: python 09_async_for.py

核心概念:
  - __aiter__ 返回异步迭代器
  - __anext__ 异步获取下一个值，结束时抛 StopAsyncIteration
  - 用 async for 来遍历异步数据流

学习笔记:
  1. 普通迭代器: __iter__ + __next__ + for
  2. 异步迭代器: __aiter__ + __anext__ + async for
  3. 典型场景：WebSocket 消息流、实时数据推送、分页 API
"""
import asyncio
import random


class AsyncNumberStream:
    """模拟异步数据流（如 WebSocket 消息）"""

    def __init__(self, count):
        self.count = count

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.count <= 0:
            raise StopAsyncIteration  # 结束信号
        self.count -= 1
        await asyncio.sleep(0.3)  # 模拟网络延迟
        return random.randint(1, 100)


async def main():
    print("  接收异步数据流:")
    async for num in AsyncNumberStream(5):
        print(f"  <- 收到数据: {num}")
    print("  数据流结束\n")

    # 实际应用：收集所有数据
    print("  收集所有数据到列表:")
    data = [num async for num in AsyncNumberStream(3)]
    print(f"  收集结果: {data}")

    # 实际应用：带条件过滤
    print("\n  只接收大于50的数据:")
    async for num in AsyncNumberStream(10):
        if num > 50:
            print(f"  -> 符合条件: {num}")


if __name__ == "__main__":
    asyncio.run(main())

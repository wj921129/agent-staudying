"""
【入门1】最基础的 async/await
==============================
运行方式: python 01_basic.py

核心概念:
  - async def 定义一个协程函数（coroutine）
  - await 用于等待一个异步操作完成
  - asyncio.run() 是程序的入口，用来启动事件循环

学习笔记:
  1. 普通函数用 def 定义，协程函数用 async def 定义
  2. 协程函数不能直接调用，必须用 await 来等待它执行
  3. await 只能在 async def 函数内部使用
  4. asyncio.run() 是最顶层的入口，它负责创建事件循环并运行协程
"""
import asyncio
from utils import print_with_time


async def say_hello():
    """最简单的协程函数"""
    print_with_time("你好，异步世界！")
    await asyncio.sleep(2)
    print_with_time("结束吧，异步世界！")
    return "hello"

async def say_hello2():
    """最简单的协程函数"""
    print_with_time("1是")
    await asyncio.sleep(1.5)
    print_with_time("2是")
    return "不hello"

async def main():
    # 使用 asyncio.gather() 并发执行多个协程
    result, result2 = await asyncio.gather(
        say_hello(),
        say_hello2()
    )
    print(f"返回值: {result}")
    print(f"返回值2: {result2}")

    # 试试看：如果不用 await 会怎样？
    # coro = say_hello()  # 这不会执行！只会得到一个 coroutine 对象
    # print(coro)         # <coroutine object say_hello at 0x...>


if __name__ == "__main__":
    asyncio.run(main())
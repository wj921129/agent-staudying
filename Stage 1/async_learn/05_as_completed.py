"""
【进阶2】as_completed —— 谁先完成谁先处理
============================================
运行方式: python 05_as_completed.py

核心概念:
  - gather 等所有任务完成，按传入顺序返回
  - as_completed 谁先完成就先拿到谁的结果
  - 适合：需要尽快处理已完成结果的场景

学习笔记:
  1. as_completed 返回的是迭代器，每个 yield 一个完成的协程
  2. 必须用 for + await 来逐个获取结果
  3. 和 gather 的区别：gather 要等全部完成，as_completed 来一个处理一个
"""
import asyncio


async def fetch_data(name, delay):
    """模拟网络请求"""
    print(f"  [{name}] 开始（需 {delay}s）...")
    await asyncio.sleep(delay)
    print(f"  [{name}] 完成！")
    return name


async def main():
    tasks = [
        asyncio.create_task(fetch_data("慢接口", 3)),
        asyncio.create_task(fetch_data("快接口", 0.5)),
        asyncio.create_task(fetch_data("中接口", 1.5)),
    ]

    print("  按完成顺序接收（不是按创建顺序）:")
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"  -> 立刻处理: {result}")

    print("\n  对比 gather: 要等3秒后才能一次性处理")
    print("  as_completed: 0.5秒后就能处理第一个结果")


if __name__ == "__main__":
    asyncio.run(main())

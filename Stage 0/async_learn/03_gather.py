"""
【入门3】asyncio.gather —— 并发执行多个协程
==============================================
运行方式: python 03_gather.py

核心概念:
  - asyncio.gather() 让多个协程同时运行
  - 全部完成后返回结果列表（按传入顺序）
  - 总耗时 = 最慢的那个任务的时间

学习笔记:
  1. gather 是最常用的并发工具，适合"同时请求多个接口"的场景
  2. 结果是按传入顺序返回的，不是按完成顺序
  3. 对比串行: 串行 1+2+1.5=4.5s -> 并发只要 2s（最慢的那个）
"""
import asyncio
import time


async def slow_task(name, seconds):
    """模拟一个耗时任务"""
    print(f"  [{name}] 开始，预计 {seconds} 秒...")
    await asyncio.sleep(seconds)
    print(f"  [{name}] 完成！")
    return f"{name} 的结果"


async def main():
    print("--- 并发执行：同时启动所有任务 ---")
    start = time.time()

    results = await asyncio.gather(
        slow_task("任务A", 1),
        slow_task("任务B", 2),
        slow_task("任务C", 1.5),
    )

    elapsed = time.time() - start
    print(f"并发总耗时: {elapsed:.1f}s（取决于最慢的2秒任务）")
    print(f"所有结果: {results}")
    print(f"结果数量: {len(results)}")


if __name__ == "__main__":
    asyncio.run(main())

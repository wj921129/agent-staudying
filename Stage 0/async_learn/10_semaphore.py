"""
【进阶7】Semaphore —— 控制并发数
====================================
运行方式: python 10_semaphore.py

核心概念:
  - Semaphore(n) 限制最多 n 个任务同时运行
  - 获取信号量 -> 执行任务 -> 释放信号量
  - 像"停车场"：有 n 个车位，满了就排队等

学习笔记:
  1. 为什么需要？防止同时发太多请求压垮服务器/被封IP
  2. async with semaphore 会自动获取和释放
  3. 结合 gather 使用：创建所有任务，但只有 N 个同时跑
"""
import asyncio
import time


async def limited_request(name, semaphore):
    """受信号量限制的请求"""
    async with semaphore:  # 获取信号量，没有就等待
        print(f"  [{name}] 进入（获取到信号量）")
        await asyncio.sleep(1)
        print(f"  [{name}] 完成（释放信号量）")
        return name


async def main():
    # 场景：6个请求，最多2个同时执行
    sem = asyncio.Semaphore(2)

    print("  并发限制: 最多 2 个同时执行")
    start = time.time()

    tasks = [limited_request(f"请求{i}", sem) for i in range(1, 7)]
    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start
    print(f"\n  总耗时: {elapsed:.1f}s")
    print(f"  分析: 6个请求 / 每次2个 = 需要3轮 = 约3秒")
    print(f"  结果: {results}")

    # 对比：如果限制为 3
    print("\n--- 对比：并发限制改为 3 ---")
    sem3 = asyncio.Semaphore(3)
    start = time.time()
    tasks = [limited_request(f"请求{i}", sem3) for i in range(1, 7)]
    await asyncio.gather(*tasks)
    print(f"  限制3个时耗时: {time.time() - start:.1f}s（6/3=2轮=约2秒）")


if __name__ == "__main__":
    asyncio.run(main())

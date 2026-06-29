"""
【入门2】asyncio.sleep —— 模拟耗时操作
==========================================
运行方式: python 02_sleep.py

核心概念:
  - asyncio.sleep() 是异步等待，不会阻塞事件循环
  - time.sleep()  是同步等待，会阻塞整个线程
  - 这是理解"异步"与"同步"区别的最关键一步

学习笔记:
  1. asyncio.sleep(n) = "等 n 秒，但等待期间可以做别的事"
  2. time.sleep(n)    = "等 n 秒，期间什么都不能做"
  3. 串行执行多个 await = 一个做完再做下一个（时间叠加）
"""
import asyncio
import time


async def slow_task(name, seconds):
    """模拟一个耗时任务"""
    print(f"  [{name}] 开始，预计 {seconds} 秒...")
    await asyncio.sleep(seconds)  # 异步等待，不阻塞
    print(f"  [{name}] 完成！")
    return f"{name} 的结果"


async def main():
    print("--- 串行执行：一个做完再做下一个 ---")
    start = time.time()

    r1 = await slow_task("任务A", 1)
    r2 = await slow_task("任务B", 2)

    elapsed = time.time() - start
    print(f"串行总耗时: {elapsed:.1f}s（1+2=3秒）")
    print(f"结果: {r1}, {r2}")

    # 思考：能不能让它们同时执行？
    # 答案在下一课 -> 03_gather.py


if __name__ == "__main__":
    asyncio.run(main())

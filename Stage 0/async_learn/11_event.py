"""
【进阶8】Event —— 协程间的信号通知
=====================================
运行方式: python 11_event.py

核心概念:
  - Event 是一个信号标志，初始为 False
  - event.set()  -> 设置信号为 True，唤醒所有等待者
  - event.wait() -> 等待信号变为 True
  - event.clear() -> 重置信号为 False

学习笔记:
  1. 典型场景：多个协程等待某个条件就绪后才开始
  2. 类似"红绿灯"：set() 变绿灯，wait() 等绿灯
  3. 一个 set() 可以唤醒多个 wait() 中的协程
"""
import asyncio


async def worker(name, event):
    """等待信号后开始工作"""
    print(f"  [{name}] 等待信号...")
    await event.wait()  # 阻塞，直到 event.set() 被调用
    print(f"  [{name}] 收到信号，开始工作！")
    await asyncio.sleep(0.5)
    print(f"  [{name}] 工作完成")


async def signaler(event):
    """发送信号"""
    await asyncio.sleep(1)
    print("  [信号发送者] 发出信号！所有等待者将被唤醒")
    event.set()


async def main():
    event = asyncio.Event()

    # 3个worker等待信号，signaler在1秒后发出信号
    await asyncio.gather(
        worker("工人A", event),
        worker("工人B", event),
        worker("工人C", event),
        signaler(event),
    )

    # 进阶：clear() 重置信号，可以重复使用
    print("\n--- 重置信号后的演示 ---")
    event.clear()
    print(f"  信号状态: {event.is_set()}")
    event.set()
    print(f"  信号状态: {event.is_set()}")
    event.clear()
    print(f"  信号状态: {event.is_set()}")


if __name__ == "__main__":
    asyncio.run(main())

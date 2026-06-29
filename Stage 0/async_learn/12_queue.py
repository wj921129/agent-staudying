"""
【进阶9】Queue —— 生产者消费者模式
=====================================
运行方式: python 12_queue.py

核心概念:
  - asyncio.Queue 是异步安全的队列
  - put() 放入数据（满了就等待）
  - get() 取出数据（空了就等待）
  - task_done() + join() 等待所有任务处理完毕

学习笔记:
  1. 生产者消费者是经典并发模式
  2. maxsize 控制队列缓冲大小，防止内存溢出
  3. queue.join() 等待所有 task_done() 被调用
  4. 消费者通常是死循环，需要在生产完成后 cancel 掉
"""
import asyncio
import random


async def producer(queue, name, count):
    """生产者：往队列里放数据"""
    for i in range(count):
        item = f"{name}-产品{i}"
        await queue.put(item)  # 队列满了会等待
        print(f"  [生产者{name}] 生产了 {item}")
        await asyncio.sleep(random.uniform(0.2, 0.5))
    print(f"  [生产者{name}] 生产完毕")


async def consumer(queue, name):
    """消费者：从队列里取数据（死循环）"""
    while True:
        item = await queue.get()  # 队列空了会等待
        print(f"  [消费者{name}] 消费了 {item}")
        await asyncio.sleep(random.uniform(0.3, 0.8))
        queue.task_done()  # 重要：标记这个 item 已处理


async def main():
    queue = asyncio.Queue(maxsize=5)  # 最多缓冲5个

    # 启动生产者
    producers = asyncio.gather(
        producer(queue, "A", 3),
        producer(queue, "B", 3),
    )

    # 启动消费者（2个消费者并行处理）
    consumers = asyncio.gather(
        consumer(queue, "甲"),
        consumer(queue, "乙"),
    )

    # 等待所有生产者完成
    await producers

    # 等待队列中所有 item 被消费
    await queue.join()

    # 取消消费者（它们是死循环，不取消会永远等下去）
    consumers.cancel()
    try:
        await consumers
    except asyncio.CancelledError:
        pass

    print("  所有产品已消费完毕！")


if __name__ == "__main__":
    asyncio.run(main())

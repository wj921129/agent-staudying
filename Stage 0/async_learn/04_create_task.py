"""
【进阶1】Task 的创建与管理
==============================
运行方式: python 04_create_task.py

核心概念:
  - asyncio.create_task() 立即调度协程（不等待）
  - gather 内部也会创建 task，但 create_task 更灵活
  - 适合：需要先启动任务，然后做别的事，最后再等结果

学习笔记:
  1. create_task 调用后任务就"开始了"，不用等 await
  2. 可以在 create_task 和 await 之间插入其他逻辑
  3. task 对象有 .done()、.result()、.cancel() 等方法
"""
import asyncio


async def fetch_data(url, delay):
    """模拟网络请求"""
    print(f"  请求 {url} 开始...")
    await asyncio.sleep(delay)
    print(f"  请求 {url} 完成！")
    return {"url": url, "status": 200}


async def main():
    # 第1步：先创建所有 task（它们立即开始运行）
    task1 = asyncio.create_task(fetch_data("https://api1.com", 1))
    task2 = asyncio.create_task(fetch_data("https://api2.com", 2))
    task3 = asyncio.create_task(fetch_data("https://api3.com", 0.5))

    # 第2步：在等待结果之前，可以做其他事情
    print("  任务已调度，先做点别的...")
    print(f"  task1 完成了吗？{task1.done()}")

    # 第3步：等待所有 task 完成
    results = await asyncio.gather(task1, task2, task3)
    for r in results:
        print(f"  结果: {r}")

    # 进阶：单个 task 的操作
    task_x = asyncio.create_task(fetch_data("单独任务", 0.1))
    await task_x  # 等待完成
    print(f"  单独结果: {task_x.result()}")
    print(f"  是否完成: {task_x.done()}")


if __name__ == "__main__":
    asyncio.run(main())

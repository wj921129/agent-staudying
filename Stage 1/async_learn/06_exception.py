"""
【进阶3】异步异常处理
========================
运行方式: python 06_exception.py

核心概念:
  - 异步代码中异常处理方式1: 普通 try/except
  - 异步代码中异常处理方式2: gather + return_exceptions=True
  - return_exceptions=True 让异常变成返回值，不会中断其他任务

学习笔记:
  1. 单个协程抛异常 -> 用 try/except 包裹 await
  2. gather 中某个任务抛异常 -> 默认会取消所有其他任务！
  3. 加 return_exceptions=True 后，异常作为结果返回，其他任务不受影响
"""
import asyncio
import random


async def risky_task(name, should_fail=False):
    """可能失败的任务"""
    await asyncio.sleep(random.uniform(0.3, 0.8))
    if should_fail:
        raise ValueError(f"[{name}] 出错了！")
    return f"[{name}] 成功"


async def main():
    # 方式1: 单个任务的 try/except
    print("--- 方式1: try/except 包裹单个 await ---")
    try:
        result = await risky_task("危险任务", should_fail=True)
        print(f"  结果: {result}")
    except ValueError as e:
        print(f"  捕获异常: {e}")

    # 方式2: gather + return_exceptions=True
    print("\n--- 方式2: gather + return_exceptions=True ---")
    results = await asyncio.gather(
        risky_task("任务A"),
        risky_task("任务B", should_fail=True),  # 这个会失败
        risky_task("任务C"),
        return_exceptions=True,
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"  异常: {r}")
        else:
            print(f"  成功: {r}")

    # 方式3: 不加 return_exceptions 会怎样？（取消注释试试）
    # print("\n--- 方式3: 不加 return_exceptions（危险！） ---")
    # results = await asyncio.gather(
    #     risky_task("任务A"),
    #     risky_task("任务B", should_fail=True),  # 这个失败会中断全部
    #     risky_task("任务C"),
    # )


if __name__ == "__main__":
    asyncio.run(main())

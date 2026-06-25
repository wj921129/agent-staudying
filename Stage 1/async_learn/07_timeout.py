"""
【进阶4】超时控制
====================
运行方式: python 07_timeout.py

核心概念:
  - asyncio.wait_for() 给协程设置超时时间
  - asyncio.timeout() (Python 3.11+) 用上下文管理器方式设置超时
  - 超时后抛出 TimeoutError，可以捕获处理

学习笔记:
  1. 网络请求不能无限等待，必须设置超时
  2. wait_for 是最常用的方式，timeout 参数单位为秒
  3. Python 3.11+ 推荐用 async with asyncio.timeout()
"""
import asyncio


async def slow_api_call():
    """模拟一个很慢的 API（要10秒）"""
    await asyncio.sleep(10)
    return "终于返回了"


async def main():
    # 方式1: asyncio.wait_for
    print("--- 方式1: asyncio.wait_for ---")
    try:
        result = await asyncio.wait_for(slow_api_call(), timeout=2.0)
        print(f"  结果: {result}")
    except asyncio.TimeoutError:
        print("  超时了！2秒内没有完成，已自动取消")

    # 方式2: asyncio.timeout (Python 3.11+)
    print("\n--- 方式2: asyncio.timeout (Python 3.11+) ---")
    try:
        async with asyncio.timeout(2.0):
            result = await slow_api_call()
            print(f"  结果: {result}")
    except TimeoutError:
        print("  超时了！(asyncio.timeout 方式)")

    # 实际应用：给每个请求设置不同超时
    print("\n--- 实际应用 ---")
    timeouts = {"登录接口": 5, "支付接口": 10, "通知接口": 3}
    for name, timeout in timeouts.items():
        print(f"  {name} 超时设置: {timeout}秒")


if __name__ == "__main__":
    asyncio.run(main())

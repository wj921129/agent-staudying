"""
【进阶5】异步上下文管理器 (async with)
=========================================
运行方式: python 08_async_with.py

核心概念:
  - __aenter__ 进入时执行的异步操作（如建立连接）
  - __aexit__ 退出时执行的异步操作（如关闭连接）
  - 用法和 with 语句一样，只是多了 async/await

学习笔记:
  1. 普通上下文管理器: __enter__ + __exit__ + with
  2. 异步上下文管理器: __aenter__ + __aexit__ + async with
  3. 典型场景：数据库连接、文件读写、网络会话
"""
import asyncio


class AsyncDBConnection:
    """模拟异步数据库连接"""

    async def __aenter__(self):
        print("  [DB] 正在建立连接...")
        await asyncio.sleep(0.5)
        print("  [DB] 连接成功！")
        return self  # 返回值绑定到 as 后面的变量

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("  [DB] 正在关闭连接...")
        await asyncio.sleep(0.3)
        print("  [DB] 连接已关闭")
        return False  # False = 不吞掉异常，True = 吞掉异常

    async def query(self, sql):
        print(f"  [DB] 执行: {sql}")
        await asyncio.sleep(0.5)
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


async def main():
    # 使用异步上下文管理器
    async with AsyncDBConnection() as db:
        rows = await db.query("SELECT * FROM users")
        print(f"  查询结果: {rows}")
        # 退出 async with 块时，自动调用 __aexit__ 关闭连接

    print("\n  即使中间出错，连接也会被关闭:")
    try:
        async with AsyncDBConnection() as db:
            raise RuntimeError("模拟错误！")
    except RuntimeError as e:
        print(f"  捕获到: {e}")
        print("  但连接已经安全关闭了")


if __name__ == "__main__":
    asyncio.run(main())

"""
【进阶10】综合实战 —— 模拟并发下载器
========================================
运行方式: python 13_real_world.py

核心概念:
  - 综合运用前面所有知识:
    create_task + Semaphore + as_completed + 异常处理 + 超时
  - 这是实际项目中非常常见的模式

学习笔记:
  1. 实际项目中的并发下载一定会限制并发数
  2. 用 as_completed 可以实时看到进度
  3. 加上超时控制，避免某个下载卡死
"""
import asyncio
import time
import random


async def download_file(url, semaphore, timeout=5.0):
    """下载单个文件（带信号量限制和超时）"""
    async with semaphore:
        delay = random.uniform(0.5, 2.0)
        print(f"  下载 {url} 开始（预计 {delay:.1f}s）")

        try:
            await asyncio.wait_for(asyncio.sleep(delay), timeout=timeout)
            size = random.randint(100, 999)
            print(f"  下载 {url} 完成（{size}KB）")
            return {"url": url, "size": size, "status": "success"}
        except asyncio.TimeoutError:
            print(f"  下载 {url} 超时！")
            return {"url": url, "size": 0, "status": "timeout"}


async def download_all(urls, max_concurrent=3, timeout=5.0):
    """并发下载所有文件"""
    sem = asyncio.Semaphore(max_concurrent)
    tasks = [
        asyncio.create_task(download_file(url, sem, timeout))
        for url in urls
    ]

    results = []
    for coro in asyncio.as_completed(tasks):
        result = await coro
        results.append(result)

    return results


async def main():
    urls = [
        "https://example.com/file1.zip",
        "https://example.com/file2.zip",
        "https://example.com/file3.zip",
        "https://example.com/file4.zip",
        "https://example.com/file5.zip",
    ]

    print(f"  共 {len(urls)} 个文件，最大并发 3，超时 5s")
    print("-" * 50)

    start = time.time()
    results = await download_all(urls, max_concurrent=3, timeout=5.0)
    elapsed = time.time() - start

    print("-" * 50)
    print(f"  全部完成！耗时 {elapsed:.1f}s")

    # 统计结果
    success = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "timeout"]
    total_size = sum(r["size"] for r in results)

    print(f"  成功: {len(success)} 个")
    print(f"  失败: {len(failed)} 个")
    print(f"  总大小: {total_size}KB")


if __name__ == "__main__":
    asyncio.run(main())

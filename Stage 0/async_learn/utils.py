import time
import asyncio

def print_with_time(msg):
    print(f"{time.strftime('%H:%M:%S', time.localtime(time.time()))} {msg}")

async def test_async():
    await asyncio.sleep(2)
    print_with_time("异步测试")

async def main():
    print_with_time("同步测试")
    task_x = asyncio.create_task(test_async())
    await task_x
    print_with_time("同步测试结束")

if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())

import asyncio
import itertools as it
import os
import random
import time


async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()


async def randsleep(a: int = 1, b: int = 5, caller=None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f'{caller} sleeping for {i} seconds.')
    await asyncio.sleep(i)


async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):
        await randsleep(caller=f'Producer {name}')
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f'Producer {name} added <{i}> to queue.')


async def consume(name: int, q: asyncio.Queue) -> None:
    print(f'Start consumer {name}')
    while True:
        await randsleep(caller=f'Consumer {name}')
        i, t = await q.get()
        now = time.perf_counter()
        print(f'Consumer {name} got element <{i}> in {now - t: 0.5f} seconds.')
        q.task_done()


async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q))
                 for n in range(nprod)]  # Start producers
    consumers = [asyncio.create_task(consume(n, q))
                 for n in range(ncon)]  # Start consumers
    await asyncio.gather(*producers)  # Wait for all producers to return
    await q.join()  # Implicitly await consumers, too; wait for all items in the queue that have been put() to be get() and task_done()
    for c in consumers:
        c.cancel()

if __name__ == "__main__":
    import argparse
    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--nprod", type=int, default=5)
    parser.add_argument("-c", "--ncon", type=int, default=10)
    args = parser.parse_args()
    start = time.perf_counter()
    asyncio.run(main(**args.__dict__))
    elapsed = time.perf_counter() - start
    print(f'Program completed in {elapsed:0.5f} seconds.')

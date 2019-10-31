import sys
import asyncio
import random


async def count():
    print('one')
    await asyncio.sleep(1)
    print('two')


async def main():
    await asyncio.gather(count(), count(), count())

# ANSI colors
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)


async def makerandom(idx: int, threshold: int = 6) -> int:
    print(c[idx + 1] + f'Initiated makerandom({idx}).')
    i = random.randint(0, 10)
    while i <= threshold:
        print(f'{c[idx + 1]} + makerandom({idx}) == {i} too low; retrying.')
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    print(f'{c[idx + 1]} --> Finished: makerandom({idx}) == {i} {c[0]}')
    return i


async def main2():
    res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3)))
    return res

if __name__ == '__main__2':
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f'{__file__} executed in {elapsed:0.2f} seconds')

if __name__ == '__main__3':
    random.seed(444)
    r1, r2, r3 = asyncio.run(main2())
    print()
    print(f'{r1} {r2} {r3}')


def f(b, a):
    print(f'b = {b}, a = {a}')


if __name__ == '__main__4':
    print(*[1, 2, 3])
    f(**{'a': 1, 'b': 2})


async def part1(n: int) -> str:
    i = random.randint(0, 10)
    print(f"part1({n}) sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f"result{n}-1"
    print(f"Returning part1({n}) == {result}.")
    return result


async def part2(n: int, arg: str) -> str:
    i = random.randint(0, 10)
    print(f"part2{n, arg} sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f"result{n}-2 derived from {arg}"
    print(f"Returning part2{n, arg} == {result}.")
    return result


async def chain(n: int) -> None:
    start = time.perf_counter()
    p1 = await part1(n)
    p2 = await part2(n, p1)
    end = time.perf_counter() - start
    print(f"-->Chained result{n} => {p2} (took {end:0.2f} seconds).")


async def main4(*args):
    await asyncio.gather(*(chain(n) for n in args))

if __name__ == '__main__':
    import sys
    import time
    random.seed(444)
    args = [1, 2, 3] if len(sys.argv) == 1 else map(int, sys.argv[1:])
    start = time.perf_counter()
    asyncio.run(main4(*args))
    end = time.perf_counter() - start
    print(f"Program finished in {end:0.2f} seconds.")


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain']
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world ! lol'
    })

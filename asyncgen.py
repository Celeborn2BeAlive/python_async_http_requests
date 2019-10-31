import asyncio


async def mygen(name, u: int = 10):
    print(f'Start {name}')
    for i in range(u):
        yield 2 ** i
        print(f'Sleep {name}')
        await asyncio.sleep(0.1)


async def make_g():
    return [i async for i in mygen("g")]


async def make_f():
    return [j async for j in mygen("f") if not (j // 3 % 5)]


async def main():
    # make_g() and make_f() are run concurrently, thanks to async for
    return await asyncio.gather(make_g(), make_f())

g, f = asyncio.run(main())
print(g)
print(f)

import requests  # not required for async example, but used for tests
import logging
import sys
import re  # regexp module
import pathlib
import asyncio

from typing import IO

import urllib.error
import urllib.parse

import aiofiles
import aiohttp
from aiohttp import ClientSession

# Globals

assert sys.version_info >= (3, 8)

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr
)
logger = logging.getLogger('async_requests')
#logging.getLogger("chardet.charsetprober").disabled = True

HREF_RE = re.compile(r'href="(.*?)"')

# Program


async def main():
    parent_path = pathlib.Path(__file__).parent

    async with aiofiles.open(parent_path.joinpath('urls.txt')) as f:
        urls = await async_set(async_map(str.strip, f))

    outpath = parent_path.joinpath("foundurls.txt")
    async with aiofiles.open(outpath, 'w') as outfile:
        await outfile.write("source_url\tparsed_url\n")

    await bulk_crawl_and_write(file=outpath, urls=urls)


async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:
    async with ClientSession() as session:
        await asyncio.gather(*(write_one(file=file, url=url, session=session, **kwargs)
                               for url in urls))


async def write_one(file: IO, url: str, **kwargs) -> None:
    res = await parse(url=url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, 'a') as f:
        for p in res:
            await f.write(f'{url}\t{p}\n')
        logger.info(f'Wrote results for source URL: {url}')


async def parse(url: str, session: ClientSession, **kwargs) -> set:
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError) as e:
        logger.error(
            f'aiohttp exception for {url} [{getattr(e, "status", None)}]: {getattr(e, "message", None)}')
        return None
    except Exception as e:
        logger.exception(
            f'Non-aiohttp exception occured {getattr(e, "__dict__", {})}')
        return None

    found = set()
    for link in HREF_RE.findall(html):
        try:
            abslink = urllib.parse.urljoin(url, link)
        except (urllib.error.URLError, ValueError):
            logger.exception(f'Error parsing URL {link}')
            continue
        found.add(abslink)
    logger.info(f'Found {len(found)} links for {url}')
    return found


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    res = await session.request(method='GET', url=url, **kwargs)
    res.raise_for_status()
    logger.info(f'Got response [{res.status}] for URL: {url}')
    return await res.text()

# Utility functions


async def async_set(async_it) -> set:
    s = set()
    async for x in async_it:
        s.add(x)
    return s


async def async_map(f, async_it):
    async for x in async_it:
        yield f(x)


async def main2():
    # not working behind proxy ? or maybe something else
    # see https://github.com/aio-libs/aiohttp/issues/3672
    async with ClientSession() as session:
        resp = await session.request(method='GET', url='https://regex101.com/')
        print(await resp.text())

    return

    async with ClientSession() as session:
        h = await fetch_html('https://regex101.com/', session=session)
        print(h)

if __name__ == '__main__':
    asyncio.run(main2())

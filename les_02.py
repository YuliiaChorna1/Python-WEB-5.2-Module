# async http client with session

import time
import aiohttp
import asyncio

async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return (await response.text())[:15]
            else:
                return f"Error {response.status}"
    
    except aiohttp.ServerTimeoutError as error:
        return str(error)
    
    except aiohttp.ClientConnectionError as error: # basic error for aiohttp (like Exception)
        return str(error)

async def main():
    url: str = "http://google.com"
    # url: str = "http://localhost:5000"

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        res: list = await asyncio.gather(
            *([fetch_url(session, url) for _ in range(10)])
        )
        print(res)

    print(f"It took: {time.time() - start_time}")

if __name__ == '__main__':
    asyncio.run(main())


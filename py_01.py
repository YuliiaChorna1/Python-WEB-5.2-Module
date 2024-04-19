# Приклад асинхронного запиту на адресу https://python.org:

import aiohttp
import asyncio
import platform


async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get("http://python.org") as responce:
            print("Status:", responce.status)
            print("Content-type:", responce.headers["content-type"])

            html = await responce.text()
            print("Body:", html[:15], "...")


if __name__ == '__main__':
    # це використовуємо, щоб уникнути помилки RuntimeError: Event loop is closed в системі Windows
    if platform.system() == "Windows": 
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
    

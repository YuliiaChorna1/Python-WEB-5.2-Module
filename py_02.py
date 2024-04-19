# запит на публічне API Приватбанку, щодо поточного курсу валют:

import aiohttp
import asyncio
import platform


async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5") as responce:
            
            print("Status: ", responce.status)
            print("Content-type: ", responce.headers["content-type"])
            print("Cookies: ", responce.cookies)
            print(responce.ok)
            result = await responce.json()
            return result
        
if __name__ == '__main__':
    if platform.system() == "Windows":

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        r = asyncio.run(main())
        print(r)


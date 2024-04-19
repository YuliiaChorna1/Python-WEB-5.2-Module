# Створення сесій без менеджеру контекста (не рекомендовано)

import aiohttp
import asyncio
import platform

async def main():
    session = aiohttp.ClientSession()
    responce = await session.get("https://python.org")

    print("Status: ", responce.status)
    print("Content-type: ", responce.headers["content-type"])

    html = await responce.text()
    responce.close() # тут ми самостійно закриваємо об'єкт response

    await session.close() # тут ми самостійно закриваємо об'єкт сесії 
    return f"Body: {html[:15]}..."


if __name__ == '__main__':
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        r = asyncio.run(main())
        print(r)

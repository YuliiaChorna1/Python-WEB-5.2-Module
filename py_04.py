# використовувати одну сесію для з'єднання з одним сервісом — це 
# значно прискорює виконання кількох запитів на один і той самий сервіс. 
# У такому разі ви можете передавати створену сесію як аргумент у функцію:

import aiohttp
import asyncio
import platform


async def index(session: aiohttp.ClientSession) -> str:
    url = "https://python.org"
    async with session.get(url) as responce:
        print("Status: ", responce.status)
        print("Content-type: ", responce.headers["content-type"])

        html = await responce.text()
        return f"Body: {html[:15]}..."
    
async def doc(session: aiohttp.ClientSession) -> str:
    url = "https://python.org/doc/"
    async with session.get(url) as responce:
        print("Status: ", responce.status)
        print("Content-type: ", responce.headers["content-type"])

        html = await responce.text()
        return f"Body: {html[:15]}..."
    
async def main():
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(index(session), doc(session))
        return result
    

if __name__ == '__main__':
    if platform.system() == "Windows":

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)

import time
import asyncio
import websockets


async def hello(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")

    await websocket.send(f"checking database")

    await asyncio.sleep(3)

    await websocket.send(f"Some data for you, but one more check")

    await asyncio.sleep(1)

    await websocket.send(f"finish")

    # while True:
        # await asyncio.sleep(1)
        # Зависає назавжди тут, але продовжує обробляти запити від нових клієнтів
        # за рахунок переключення контексту

async def main():
    async with websockets.serve(hello, "localhost", 8765) as server:
        await server.server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown")


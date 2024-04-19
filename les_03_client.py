import asyncio
import websockets

async def hello():
    url = "ws://localhost:8765"
    async with websockets.connect(url) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f">>> {name}")

        greeting = ""
        while greeting != "finish":
            greeting = await websocket.recv()
            print(greeting)

        
if __name__ == '__main__':
    asyncio.run(hello())

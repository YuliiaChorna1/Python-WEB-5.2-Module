# Тут лише одна функція hello, яка надсилає ім'я на сервер, 
# отримує привітання та закриває з'єднання.

# Очікування з'єднання викликає WebSocketClientProtocol, який потім 
# використовується для надсилання та отримання повідомлень.


import asyncio
import websockets


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket: # відкриває з'єднання із веб-сокетом
        name = input("What's your name? ")

        await websocket.send(name)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


if __name__ == '__main__':
    asyncio.run(hello())


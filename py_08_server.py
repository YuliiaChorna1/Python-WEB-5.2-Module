# Запуск сервера виконується командою asyncio.run(main()). 
# Сама функція main за допомогою асинхронного контексту створює сервер WebSocket
# командою websockets.serve(hello, "localhost", 8765). 

# Аргумент hello – це функція обробник повідомлень між сервером та клієнтом, 
# аргумент `localhost' визначає хост для сервера, а 
# 8765 – порт, на якому буде встановлено з'єднання.

# У функції hello ми отримуємо параметр websocket, що має тип WebSocketServerProtocol. 
# Отримуємо повідомлення від клієнта за допомогою name = await websocket.recv(), 
# а відправляємо повідомлення виразом await websocket.send(greeting). 
# по суті, це ехо-сервер.

import asyncio
import websockets


async def hello(websocket): # websocket: WebSocketServerProtocol
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future() # run forever


if __name__ == '__main__':
    asyncio.run(main())

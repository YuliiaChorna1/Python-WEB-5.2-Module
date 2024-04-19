# простий споживач повід. від Websocket сервера (слухає та отримує повід. від сервера Websocket)
# Тут за допомогою функції consumer ми підключаємося до віддаленого Websocket сервера
# на порту 4000. Як і раніше, через асинхронний контекст підключення, 
# отримуємо екземпляр ws класу WebSocketClientProtocol
# Далі за допомогою асинхронного циклу async for ми виконуватимемо перебір асинхронного
# ітератора ws і логуємо отримані повідомлення.

import asyncio
import logging
import websockets

logging.basicConfig(level=logging.INFO)

async def consumer(hostname: str, port: int):
    ws_resourse_url = f"ws://{hostname}:{port}"
    async with websockets.connect(ws_resourse_url) as ws:
        async for message in ws:
            logging.info(f"Message: {message}")


if __name__ == '__main__':
    asyncio.run(consumer("localhost", 4001))


# Цей сервер є класом Server, який поєднує весь функціонал сервера: розсилає повідомлення, 
# надіслані producer, всім слухачам consumer.

# Екземпляр класу Server має асинхронну функцію ws_handler, яка і визначає співпрограму 
# оброблювача веб-сокета. При підключенні клієнта, функція ws_handler приймає з'єднання, 
# створює екземпляр ws класу WebSocketServerProtocol і здійснює "рукостискання" (handshake). 
# Далі ми запам'ятовуємо екземпляр клієнта за допомогою функції register і поміщаємо його 
# у змінну класу clients, яка є множиною. 
# Як тільки обробник завершує роботу, нормально або за винятком WebSocketProtocolError, 
# сервер виконує закриваюче "рукостискання" та закриває з'єднання, і видаляє дані 
# про клієнта за допомогою функції unregister.

import asyncio
import logging
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set() # clients = [] # returning context to EventLoop (test)

    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        # logging.info("Send Started") # returning context to EventLoop (test)
        if self.clients:
            # logging.info("Client found") # returning context to EventLoop (test)
            for client in self.clients:
                await client.send(message)
                
    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK as ex:
            logging.info(f"{ws.remote_address} Closing connection because of error")
        finally:
            await self.unregister(ws)
            # await asyncio.sleep(0) # returning context to EventLoop (test)

    async def distribute(self, ws: WebSocketServerProtocol):
        # logging.info(f"{ws.remote_address} starts distribution") # returning context to EventLoop (test)
        async for message in ws:
            await self.send_to_clients(message)
            # await asyncio.sleep(0) # returning context to EventLoop (test)


async def main():
    server = Server()

    async with websockets.serve(server.ws_handler, "localhost", 4001):
        await asyncio.Future() # run forever


if __name__ == '__main__':
    asyncio.run(main())

# Запуск сервера призведе до виконання співпрограми main, яка запустить веб-сокет server.ws_handler. 
# Наш метод ws_handler реєструє з'єднання await self.register(ws), відправляє повідомлення 
# підключеним клієнтам await self.distrubute(ws) і, нарешті, закриває з'єднання await self.unregister(ws). 

# consumer залишається підключеним до сервера, у той час як producer скасовує власну реєстрацію.

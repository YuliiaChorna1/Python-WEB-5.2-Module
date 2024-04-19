import sys
import asyncio
import logging
import logging.config
import websockets
from pathlib import Path
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

logger = logging.getLogger("logging_test_app")

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(message)s"
        },
        "super simple": {
            "format": "%(message)s"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "super simple",
            "filename": f"logs/my_app_{Path(sys.argv[0]).name}.log",
            "maxBytes": 10000,
            "backupCount": 2
        }
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["stdout", "file"]
        }
    }
}

class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)
        logger.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logger.info(f"{ws.remote_address} disconnects")

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)
    
    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            for client in self.clients:
                if client != ws:
                    await client.send(f"{ws.remote_address}: {message}")


async def main():
    server = Server()

    async with websockets.serve(server.ws_handler, "localhost", 8765) as server:
        await server.server.serve_forever()

if __name__ == '__main__':
    logging.config.dictConfig(logging_config)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("\nShutdown")
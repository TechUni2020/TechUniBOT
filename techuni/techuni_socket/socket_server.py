import asyncio
import socket
from asyncio.events import AbstractEventLoop
from techuni import JoinApplication

class SocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self._soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._soc.setblocking(False)
        self._soc.bind((host, port))
        self._soc.listen()
        self._loop = None

    async def handle_client(self, client: socket.socket, loop: AbstractEventLoop):
        while _data := await loop.sock_recv(client, 1024):
            data = _data.decode("utf-8")
            app = JoinApplication.from_socket(data)

            if app is None:
                await loop.sock_sendall(client, b"Invalid Data.")
                print("Invalid Data.")
                continue

            print(f"data = {str(app)}")
            await loop.sock_sendall(client, b"OK.")
        client.close()

    async def start(self):
        self._loop = asyncio.get_event_loop()
        while True:
            client, addr = await self._loop.sock_accept(self._soc)
            client.setblocking(False)
            print(f"New Socket Connection from {addr}")
            await asyncio.create_task(self.handle_client(client, self._loop))

import os
import asyncio
from multiprocessing import Process, Queue
from techuni.techuni_discord import TechUniDiscordBot
from techuni.techuni_socket import SocketServer
from techuni.techuni_email import EmailTemplate

def socket_main(queue):
    TechUniDiscordBot.socket_applier = queue
    socket_s = SocketServer("localhost", int(os.environ.get("SOCKET_PORT")))
    asyncio.run(socket_s.start())

def main():
    socket_queue = Queue()
    TechUniDiscordBot.socket_applier = socket_queue

    bot = TechUniDiscordBot()

    socket_process = Process(target=socket_main, args=(socket_queue,))
    socket_process.start()

    EmailTemplate.load()

    bot.run(str(os.environ.get("DISCORD_BOT_TOKEN")))

    socket_process.join()

if __name__ == "__main__":
    main()

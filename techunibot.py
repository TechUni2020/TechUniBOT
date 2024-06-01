import os
import asyncio
from multiprocessing import Process, Queue
from techuni.techuni_discord import TechUniDiscordBot
from techuni.techuni_socket import SocketServer
from techuni.techuni_email import EmailTemplate, EmailClientManager, EmailController

def socket_main(queue):
    TechUniDiscordBot.socket_applier = queue
    socket_s = SocketServer("localhost", int(os.environ.get("SOCKET_PORT")))
    asyncio.run(socket_s.start())

def main():
    socket_queue = Queue()
    TechUniDiscordBot.socket_applier = socket_queue

    EmailTemplate.load()
    client_manager = EmailClientManager()
    email_controller = EmailController(client_manager)

    bot = TechUniDiscordBot(email_controller)

    socket_process = Process(target=socket_main, args=(socket_queue,))
    socket_process.start()

    bot.run(str(os.environ.get("DISCORD_BOT_TOKEN")))

    socket_process.join()

if __name__ == "__main__":
    main()

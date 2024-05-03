import discord
import os
from techuni import TechUniDiscordBot, SocketServer
import asyncio
from multiprocessing import Process, Queue

def socket_main(queue):
    TechUniDiscordBot.flask_applier = queue
    socket_s = SocketServer("localhost", int(os.environ.get("SOCKET_PORT")))
    asyncio.run(socket_s.start())

def main():
    socket_queue = Queue()
    TechUniDiscordBot.flask_applier = socket_queue

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = TechUniDiscordBot(intents=intents)

    socket_process = Process(target=socket_main, args=(socket_queue,))
    socket_process.start()

    bot.run(str(os.environ.get("DISCORD_BOT_TOKEN")))

    socket_process.join()

if __name__ == "__main__":
    main()

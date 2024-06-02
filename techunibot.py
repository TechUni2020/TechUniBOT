import os
import asyncio
from multiprocessing import Process, Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from techuni.techuni_discord import TechUniDiscordBot
from techuni.techuni_socket import SocketServer
from techuni.techuni_database.model import JoinApplicationTable
from techuni.techuni_database import DatabaseSession

def socket_main(queue):
    TechUniDiscordBot.socket_applier = queue
    socket_s = SocketServer("localhost", int(os.environ.get("SOCKET_PORT")))
    asyncio.run(socket_s.start())

def main():
    # Database
    database_engine = create_engine(str(os.environ.get("DATABASE_URL")), echo=False)
    session_factory = sessionmaker(bind=database_engine, autoflush=True, autocommit=False)

    ## init database
    JoinApplicationTable.metadata.create_all(database_engine)

    database_session = DatabaseSession(session_factory())

    # Socket
    socket_queue = Queue()
    TechUniDiscordBot.socket_applier = socket_queue

    # Discord BOT
    bot = TechUniDiscordBot(database_session)

    # --- Process Start --- #
    # Socket
    socket_process = Process(target=socket_main, args=(socket_queue,))
    socket_process.start()

    # Discord BOT
    bot.run(str(os.environ.get("DISCORD_BOT_TOKEN")))

    socket_process.join()
    database_session.close()

if __name__ == "__main__":
    main()

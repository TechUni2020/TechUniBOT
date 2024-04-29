import discord
import os
from flask import Flask
from multiprocessing import Process, Queue

from techuni_flask import app as flask_app
from techuni_discord import TechUniDiscordBot

app = Flask(__name__)
app.register_blueprint(flask_app)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# 親ファイル
bot = TechUniDiscordBot(intents=intents)

def run_discord(discord_appliers):
    TechUniDiscordBot.flask_applier = discord_appliers  # DiscordスレッドにapplierQueueを追加
    bot.run(str(os.environ.get("DISCORD_BOT_TOKEN")))

def main():
    queue_discord_appliers = Queue()
    TechUniDiscordBot.flask_applier = queue_discord_appliers
    discord_process = Process(target=run_discord, args=(queue_discord_appliers,))

    # process start
    discord_process.start()


if __name__ == "__main__":
    main()

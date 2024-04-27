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
_bot_config = os.path.abspath(os.path.join(os.path.dirname(__file__), "config", "discord.yml"))
bot = TechUniDiscordBot(intents=intents, path_config_file=_bot_config)

def run_flask(discord_appliers):
    TechUniDiscordBot.flask_applier = discord_appliers  # flaskスレッドにapplierQueueを追加
    app.run()

def run_discord(discord_appliers):
    TechUniDiscordBot.flask_applier = discord_appliers  # DiscordスレッドにapplierQueueを追加
    bot.run(os.environ.get("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    queue_discord_appliers = Queue()
    flask_process = Process(target=run_flask, args=(queue_discord_appliers,))
    discord_process = Process(target=run_discord, args=(queue_discord_appliers,))

    # process start
    flask_process.start()
    discord_process.start()

    # process join(終了待ち)
    flask_process.join()
    discord_process.join()

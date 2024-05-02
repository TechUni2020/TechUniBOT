import discord
import os
from techuni import TechUniDiscordBot

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# 親ファイル
bot = TechUniDiscordBot(intents=intents)

def main():
    bot.run(str(os.environ.get("DISCORD_BOT_TOKEN")))

if __name__ == "__main__":
    main()

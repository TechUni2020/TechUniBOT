import os
from techuni import TechUniDiscordBot

# 親ファイル
bot = TechUniDiscordBot()

def main():
    bot.run(str(os.environ.get("DISCORD_BOT_TOKEN")))

if __name__ == "__main__":
    main()

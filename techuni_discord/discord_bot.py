import discord
from techuni_object import JoinApplication
class TechUniDiscordBot(discord.Client):
    async def on_ready(self):
        pass

    async def on_message(self, message):
        pass

    async def onApplyForm(self, data: JoinApply):
        pass

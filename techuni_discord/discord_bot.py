import discord
from discord.ext import tasks
from techuni_object import JoinApplication
from multiprocessing import Queue

flask_applier = Queue()

class TechUniDiscordBot(discord.Client):

    async def on_ready(self):
        print(f"Logged on as {self.user.name} ({self.user.id})")

    async def on_message(self, message):
        pass

    async def notify_application(self, application: JoinApplication):
        pass

    @tasks.loop(seconds=60)
    async def checkForm(self):
        while not flask_applier.empty():
            application: JoinApplication = flask_applier.get()
            await self.notify_application(application)

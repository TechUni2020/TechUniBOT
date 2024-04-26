import discord
from discord.ext import tasks
from techuni_object import JoinApplication
from multiprocessing import Queue
from yaml import safe_load

flask_applier = Queue()

class TechUniDiscordBot(discord.Client):
    def __init__(self, *args, path_config_file: str, **kwargs):
        super().__init__(*args, **kwargs)
        with open(path_config_file, "r") as f:
            self.config: dict = safe_load(f)

        # Load GuildID from config
        _g_uid = self.config.get("guild_id")
        if _g_uid is None:
            raise ValueError("guild_id is not found in config file")

        # Load Guild
        self.guild = self.get_guild(_g_uid)
        if self.guild is None:
            raise ValueError(f"Guild({_g_uid}) is not found")

        # Load ChannelID from config
        _chid = self.config.get("channel_id")
        if _chid is None:
            raise ValueError("channel_id is not found in config file")
        _chid_join_appl = _chid.get("join_application")
        if _chid_join_appl is None:
            raise ValueError("join_application is not found in channel_id")

        # Load Join Application Channel
        self.channel_join_appl: discord.ForumChannel = self.guild.get_channel(_chid_join_appl)
        if self.channel_join_appl is None:
            raise ValueError(f"Channel({_chid_join_appl}) is not found")
        if self.channel_join_appl is not discord.ForumChannel:
            raise ValueError(f"Channel({self.channel_join_appl.name}) is not ForumChannel")

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

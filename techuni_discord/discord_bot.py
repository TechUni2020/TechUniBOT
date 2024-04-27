import discord
from discord.ext import tasks
from techuni_object import JoinApplication
from multiprocessing import Queue
from yaml import safe_load

class TechUniDiscordBot(discord.Client):
    flask_applier: Queue = None
    def __init__(self, *args, path_config_file: str, **kwargs):
        super().__init__(*args, **kwargs)

        self.channel_join_appl = None
        self.guild = None
        with open(path_config_file, "r") as f:
            self.config: dict = safe_load(f)

    async def on_ready(self):
        print(f"Logged on as {self.user.name} ({self.user.id})")

        # Load GuildID from config
        _g_uid = int(self.config.get("guild_id"))
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
        _chid_join_appl = int(_chid.get("join_application"))
        if _chid_join_appl is None:
            raise ValueError("join_application is not found in channel_id")

        # Load Join Application Channel
        self.channel_join_appl: discord.ForumChannel = self.guild.get_channel(_chid_join_appl)
        if self.channel_join_appl is None:
            raise ValueError(f"Channel({_chid_join_appl}) is not found")
        if not isinstance(self.channel_join_appl, discord.ForumChannel):
            raise ValueError(f"Channel({self.channel_join_appl.name}) is not ForumChannel(is {type(self.channel_join_appl)})")

        checkForm_task = self.checkForm.start()
        print(f"TechUniDiscordBot is ready. {checkForm_task.get_name()}")

    async def on_message(self, message):
        pass

    async def notify_application(self, application: JoinApplication):
        await self.channel_join_appl.create_thread(
            name=application.name,
            content=application.create_initial_message(),
            allowed_mentions=discord.AllowedMentions(roles=True),
            reason=f"入会者フォーム回答({application.name} さん)"
        )

    @classmethod
    def add_application(cls, application: JoinApplication):
        if cls.flask_applier is None:
            raise ValueError("flask_applier is not set")
        cls.flask_applier.put(application)

    @tasks.loop(seconds=60)
    async def checkForm(self):
        while not self.flask_applier.empty():
            application: JoinApplication = self.flask_applier.get()
            await self.notify_application(application)

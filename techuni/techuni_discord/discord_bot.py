import discord
import os
from discord.ext import tasks, commands
from multiprocessing import Queue
from techuni.techuni_object import JoinApplication, JoinApplicationStatus
from techuni.techuni_discord.commands import JoinApplicationCommand
from techuni.techuni_discord.view import JoinApplicationDecideView

class TechUniDiscordBot(commands.Bot):
    socket_applier: Queue = None

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(intents=intents, command_prefix="/")

        self.channel_join_appl: discord.ForumChannel | None = None
        self.channel_invite: discord.abc.GuildChannel | None = None
        self.guild: discord.Guild | None = None
        self.tag_appl_receive: discord.ForumTag | None = None
        self.personal_invite_age: int | None = None

    async def on_ready(self):
        print(f"Logged on as {self.user.name} ({self.user.id})")

        # Load GuildID from config
        _g_uid = int(os.environ.get("DISCORD_GID"))
        if _g_uid is None:
            raise ValueError("guild_id is not found in config file")
        
        # Load Guild
        self.guild = self.get_guild(_g_uid)
        if self.guild is None:
            raise ValueError(f"Guild({_g_uid}) is not found")

        # Load Channel
        # Load Join Application Channel
        _chid_join_appl = int(os.environ.get("DISCORD_CHID_JOIN_APPLICATION"))
        self.channel_join_appl: discord.ForumChannel = self.guild.get_channel(_chid_join_appl)
        if self.channel_join_appl is None:
            raise ValueError(f"Channel({_chid_join_appl}) is not found")
        if not isinstance(self.channel_join_appl, discord.ForumChannel):
            raise ValueError(f"Channel({self.channel_join_appl.name}) is not ForumChannel(is {type(self.channel_join_appl)})")

        # Load Invite Channel
        _chid_invite = int(os.environ.get("DISCORD_CHID_INVITE"))
        self.channel_invite: discord.abc.GuildChannel = self.guild.get_channel(_chid_invite)
        if self.channel_invite is None:
            raise ValueError(f"Channel({_chid_invite}) is not found")

        self.personal_invite_age = int(os.environ.get("DISCORD_INVITE_AGE"))

        self.tag_appl_receive = JoinApplicationStatus.RECEIVE.get_tag(self.channel_join_appl)
        if self.tag_appl_receive is None:
            raise ValueError("Receive Tag is not found")

        self.checkForm.start()
        await self.add_cog(JoinApplicationCommand(self))
        JoinApplicationDecideView.FORUM_CHANNEL = self.channel_join_appl
        JoinApplicationDecideView.INVITE_FUNCTION = self.create_personal_invite
        print("TechUniDiscordBot is ready.")

    async def setup_hook(self):
        self.add_view(JoinApplicationDecideView())

    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        raise error

    async def create_personal_invite(self, data: JoinApplication | str) -> discord.Invite:
        if isinstance(data, JoinApplication):
            name = data.name
        elif isinstance(data, str):
            name = data
        else:
            raise ValueError("data is not JoinApplication or str")

        invite = await self.channel_invite.create_invite(
            max_age=self.personal_invite_age,
            max_uses=1,
            unique=True,
            reason=f"入会者({name}さん)への招待リンク"
        )
        return invite

    async def notify_application(self, application: JoinApplication):
        await self.channel_join_appl.create_thread(
            name=application.name,
            content=application.create_initial_message(),
            view=JoinApplicationDecideView(),
            allowed_mentions=discord.AllowedMentions(roles=True),
            applied_tags=[self.tag_appl_receive],
            reason=f"入会者フォーム回答({application.name} さん)"
        )

    @classmethod
    def add_application(cls, application: JoinApplication):
        if cls.socket_applier is None:
            raise ValueError("socket_applier is not set")
        cls.socket_applier.put(application)

    @tasks.loop(seconds=5)
    async def checkForm(self):
        while not self.socket_applier.empty():
            application: JoinApplication = self.socket_applier.get()
            await self.notify_application(application)

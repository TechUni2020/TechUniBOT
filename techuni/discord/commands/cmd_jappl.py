from discord.ext import commands
from techuni.discord.command.checker import check_guild
from techuni.discord.command.check_error import OutOfTechUniGuildError

class JoinApplicationCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jappl")
    @commands.check(check_guild)
    async def command_join_application(self, ctx: commands.Context, *arg: tuple[str]):
        pass

    @command_join_application.error
    async def cja_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("このコマンドをDirect Messageで実行することはできません。")
        elif isinstance(error, OutOfTechUniGuildError):
            await ctx.send("このコマンドはTech.Uni Discordサーバーでのみ利用可能です。")
        else:
            print(f"An error occurred. in {ctx.command.name} - {error}({error.__class__.__name__})")
            await ctx.send("An error occurred.")

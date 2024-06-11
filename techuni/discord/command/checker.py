import os
from discord.ext import commands
from techuni.discord.command.check_error import OutOfTechUniGuildError

_GID = None
def check_guild(ctx: commands.Context):
    global _GID

    if (g := ctx.guild) is None:
        raise commands.NoPrivateMessage()

    if _GID is None:
        _GID = int(os.environ.get("DISCORD_GID"))

    if g.id != _GID:
        raise OutOfTechUniGuildError()
    return True

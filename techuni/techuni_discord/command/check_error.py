from discord.ext import commands

class OutOfTechUniGuildError(commands.CommandError):
    def __init__(self):
        super().__init__("This command is only available in Tech.Uni Discord Server.")

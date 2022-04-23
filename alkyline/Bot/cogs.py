import discord
from discord.ext import commands
from .bot import Alkyline


class BaseCog(commands.Cog):
    def __init__(self, bot: Alkyline):
        self.bot = bot

    async def cog_check(self, ctx):
        return not ctx.author.bot


class StaffCog(BaseCog):
    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator


class GuildOnly(BaseCog):
    async def cog_check(self, ctx):
        return type(ctx.channel) == discord.TextChannel


class PrivateCog(BaseCog, command_attrs=dict(hidden=True)):
    pass

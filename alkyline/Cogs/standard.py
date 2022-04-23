import datetime

from ..Bot.cogs import BaseCog
from discord.ext import commands
from ..Utilities.utilities import get_date
import random
import discord
import typing
class Standard(BaseCog):
    @commands.command(aliases=["whois", "ui"],
                      description="Displays information about input user(s).")
    async def userinfo(self, ctx, *users: typing.Union[discord.Member, discord.User]):
        if len(users) == 0:
            users = [ctx.author]
        now = datetime.datetime.now()
        for user in users:
            embed = discord.Embed(title=user, description=f"ID:{user.id}").set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Created at:", value=get_date(user.created_at, show=True))
            embed.set_footer(text=f"Requested by {ctx.author} | {get_date(now)}")
            try:
                if len(user.roles) > 1:
                    roles = [role for role in user.roles if role.name != '@everyone']
                    embed.add_field(name='Roles', value="".join(r.mention for r in roles))
                embed.add_field(name="Joined at:", value=get_date(user.joined_at, show=True))
                embed.colour = user.top_role.color
            except AttributeError:
                pass
            await ctx.send(embed=embed)

    @commands.command()
    async def echo(self, ctx, *, message: str):
        await ctx.send(message)

    @commands.command()
    async def choose(self, ctx, *choices: str):
        if len(choices) == 0:
            await ctx.send(ctx.author, ", there is nothing to choose from.")
        else:
            await ctx.send("I choose `" + random.choice(choices) + "`.")

    @commands.command(aliases=["avt"])
    async def avatar(self, ctx, *users: discord.User):
        if len(users) <= 0:
            users = [ctx.author]
        for user in users:
            await ctx.send(user.avatar_url)

    @commands.command()
    async def hey(self, ctx):
        await ctx.send("heya")

    # @commands.command
    # @commands.has_permissions(administrator=True)
    # async def setprefix(self, ctx, new_prefix):
    #     self.bot.command_prefix = [new_prefix, "]"]
    #     await ctx.send(f"The prefix is now {new_prefix}.")
    #


def setup(bot):
    bot.add_cog(Standard(bot))

import discord
from discord.ext import commands
import typing
from ..Bot.cogs import StaffCog, GuildOnly


class Staff(StaffCog, GuildOnly):

    @commands.command()
    async def unban(self, ctx, user: discord.User):
        if ctx.message.author == user:
            await ctx.send(f"{ctx.author.mention}, you cannot unban yourself!")
        else:
            await ctx.guild.unban(user)
            await ctx.send(f'User {user} has been unbanned')

    @commands.command()
    async def kick(self, ctx, member: discord.Member, reason=None):
        if ctx.message.author == member:
            await ctx.send(f"{ctx.author.mention}, you cannot kick yourself!")
        else:
            await member.kick(reason=reason)
            await ctx.send(f'Member {member} has been kick for reason: {reason}')

    @commands.command()
    async def ban(self, ctx, user: typing.Union[discord.Member, discord.User], reason=None):
        if ctx.message.author == user:
            await ctx.send(f"{ctx.author.mention}, you cannot ban yourself!")
        else:
            try:
                await user.ban(reason=reason)
            except AttributeError:
                await ctx.guild.ban(user, reason=reason)
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f'User {user} has been permanently banned for reason: {reason}')
    # @commands.command()
    # async def mute(self, ctx, user:typing.Union[discord.Member, discord.User],reason=None):
    #


def setup(bot):
    bot.add_cog(Staff(bot))

import datetime
import discord
from discord.ext import commands
import typing
import random
from ..Utilities import get_date
from ..Bot.cogs import GuildOnly


class GuildCmds(GuildOnly):
    @commands.command(aliases=["svinfo", "si"],
                      description="Displays information about the current server.")
    async def serverinfo(self, ctx, *guilds: discord.Guild):
        now = datetime.datetime.now()
        if len(guilds) == 0:
            guilds = [ctx.guild]
        for guild in guilds:
            embed = (discord.Embed(
                title=f"**{guild.name} ({guild.id})**",
                description=f"Description: {guild.description}").add_field(
                name="Boosters", value=f"{guild.premium_subscription_count} (Tier {guild.premium_tier})").add_field(
                name="Members:", value=f"{len(list(filter(lambda m: not m.bot, guild.members)))}").add_field(
                name="Bots:", value=f"{len(list(filter(lambda m: m.bot, guild.members)))}").add_field(
                name="Created on:", value=get_date(guild.created_at, show=True)).add_field(
                name="Server region:", value=f"{guild.region}").add_field(
                name="Owner:", value=f"{guild.owner}")).add_field(
                name="Features:", value=f"`{','.join(guild.features)}`").set_thumbnail(
                url=guild.icon_url).set_footer(
                text=f"Requested by {ctx.author} | {get_date(now)}")
            await ctx.send(embed=embed)

    @commands.command(aliases=["chlinfo", "ci"],
                      description="Displays information about the input channels.")
    async def channelinfo(self, ctx, *channels: typing.Union[discord.TextChannel, discord.VoiceChannel]):
        if len(channels) == 0:
            channels = [ctx.channel]
        for channel in channels:
            embed = discord.Embed(
                title=f"{channel.name} ({channel.id})").add_field(
                name="Created on:", value=get_date(channel.created_at, show=True)).add_field(
                name="Position:", value=channel.position).add_field(
                # Not putting channel.type in str() creates an AttributeError
                name="Type:", value=f"{str(channel.type).capitalize()} channel").add_field(
                name="In category:", value=f"{channel.category} ({channel.category_id})").add_field(
                name="Members:", value=len(channel.members))
            try:
                embed.description = f"Topic: {channel.topic}"
                embed.add_field(
                    name="Voice communication region:", value=channel.rtc_region).add_field(
                    name="User limit:", value=channel.user_limit)
            except AttributeError:
                pass
            await ctx.send(embed=embed)

    @commands.group()
    async def role(self, ctx):
        pass

    @role.command(description="Returns information about input roles.")
    async def info(self, ctx, *roles: discord.Role):
        for r in roles:
            await ctx.send(embed=discord.Embed(title=r.name, description=r.id, color=r.color).add_field(
                name="Color:", value=r.color).add_field(
                name="Mention:", value=r.mention).add_field(
                name="Mentionable:", value=r.mentionable).add_field(
                name="Position:", value=r.position).add_field(
                name="Permission:", value=f"`{r.permissions}`").add_field(
                name="Created at:", value=get_date(r.created_at, show=True)))

    @role.command(description="Returns a list of all roles in the server.")
    async def list(self, ctx):
        role_list_1 = []
        for role_1 in ctx.guild.roles:
            if role_1.name != "@everyone":
                role_list_1.append(f"<@&{role_1.id}>")
        role_list_2 = "".join(role_list_1)
        embed = discord.Embed(title=f"{ctx.guild.name}", description=f"{len(role_list_1)}")
        embed.add_field(name="Roles:", value=f"{role_list_2}")
        await ctx.send(embed=embed)

    @role.command(description="Adds role to users.")
    @discord.ext.commands.has_permissions(manage_roles=True)
    async def add(self, ctx, r: discord.Role, *users: discord.Member):
        names = []
        for user in users:
            await user.add_roles(r)
            names.append(user.name)
        await ctx.send(f"Role `{r}` has been added to {','.join(names)}.")

    @role.command(description="Removes roles from an user.")
    @discord.ext.commands.has_permissions(manage_roles=True)
    async def remove(self, ctx, user: discord.Member, *roles: discord.Role):
        for role1 in roles:
            for role2 in user.roles:
                if role2 == role1:
                    await user.remove_roles(role2)
                    await ctx.send(f"Role `{role2}` has been removed from {user.name}.")

    @commands.command(description="Mentions an online staff member.")
    async def pingstaff(self, ctx):
        mods = []
        for member in ctx.guild.members:
            if all([member.guild_permissions.administrator, not member.bot, member.status == discord.Status.online]):
                mods.append(member)
        if len(mods) == 0:
            mods.append(ctx.guild.owner)
            mod = mods[0]
        else:
            mod = random.choice(mods)
        await ctx.send(mod.mention)

def setup(bot):
    bot.add_cog(GuildCmds(bot))

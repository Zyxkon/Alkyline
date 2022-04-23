import datetime
import random
import discord.ext
import json
from discord.ext import commands
from Zyxbot.Utilities.utilities import get_date
from ..Bot.cogs import StaffCog, GuildOnly


class ListenersCmds(StaffCog, GuildOnly):
    @discord.ext.commands.command()
    async def setwelcomechannel(self, ctx, channel: discord.TextChannel):
        if channel is not None:
            await ctx.send(f"The channel for welcome messages is now {channel.mention}.")
            with open("../Database/database.json", "r+") as json_file:
                database = json.load(json_file)
                with open('../Database/database.json', 'w') as _json_file:
                    if f"{channel.guild.id}" in database:
                        pass
                    else:
                        database[f"{channel.guild.id}"] = dict()
                    for channel_ in channel.guild.channels:
                        if channel_.id == channel.id:
                            database[f"{channel.guild.id}"]['welcome_channel'] = int(channel.id)
                            database[f"{channel.guild.id}"]['name'] = f'{channel.guild}'
                            json.dump(database, _json_file, sort_keys=True, indent=3)

    @discord.ext.commands.command()
    async def setleavechannel(self, ctx, channel: discord.TextChannel):
        if channel is not None:
            _channel = 0
            await ctx.send(f"The channel for leave messages is now {channel.mention}.")
            with open("../Database/database.json", "r") as json_file:
                database = json.load(json_file)
                with open("../Database/database.json", 'w') as _json_file:
                    if f"{channel.guild.id}" in database:
                        pass
                    else:
                        database[f"{channel.guild.id}"] = dict()
                    for channel_ in channel.guild.channels:
                        if channel_.id == channel.id:
                            database[f"{channel.guild.id}"]['leave_channel'] = int(channel.id)
                            json.dump(database, _json_file, sort_keys=True, indent=3)

    @discord.ext.commands.command()
    async def setmodlog(self, ctx, channel: discord.TextChannel):
        if channel is not None:
            _channel = 0
            await ctx.send(f"The channel for modlog is now {channel.mention}.")
            with open("../Database/database.json", "r") as json_file:
                database = json.load(json_file)
                with open("../Database/database.json", 'w') as _json_file:
                    if f"{channel.guild.id}" in database:
                        pass
                    else:
                        database[f"{channel.guild.id}"] = dict()
                    for channel_ in channel.guild.channels:
                        if channel_.id == channel.id:
                            database[f"{channel.guild.id}"]['modlog'] = int(channel.id)
                            json.dump(database, _json_file, sort_keys=True, indent=3)

    # @discord.ext.commands.command(aliases=["init"], pass_context=True)
    # async def initialize(self, ctx):
    #     with open("../database.json", "r") as json_file:
    #         database = json.load(json_file)
    #         if f"{ctx.guild.id}" in database:
    #             await ctx.send("This server's configuration has already been initialized.")
    #         else:
    #             with open("../database.json", 'w') as _json_file:
    #                 database[f"{ctx.guild.id}"] = dict()
    #                 database[f"{ctx.guild.id}"]['modlog'] = 0
    #                 database[f"{ctx.guild.id}"]['name'] = str(ctx.guild.name)
    #                 database[f"{ctx.guild.id}"]['welcome_channel'] = 0
    #                 database[f"{ctx.guild.id}"]['leave_channel'] = 0
    #                 json.dump(database, _json_file, sort_keys=True, indent=3)
    #                 await ctx.send("This server's configuration has been initialized.")

    # @discord.ext.commands.command(aliases=["trdwn"], pass_context=True)
    # @discord.ext.commands.has_permissions(administrator=True)
    # @discord.ext.commands.guild_only()
    # async def teardown(self, ctx):
    #     with open("../database.json", "r") as json_file:
    #         database = json.load(json_file)
    #         with open("../database.json", 'w') as _json_file:
    #             if f"{ctx.guild.id}" in database:
    #                 del database[f"{ctx.guild.id}"]
    #                 await ctx.send("This server's configuration has been torndown")
    #                 json.dump(database, _json_file, sort_keys=True, indent=3)
    #             else:
    #                 await ctx.send("This server's configuration has either not been initialized or already torndown")
class Listeners(GuildOnly):
    @discord.ext.commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_messages = (
            "Welcome {} to the server!",
            "{} just joined the server!",
            "Hello {}! Hope you enjoy your stay!",
        )
        with open(self.bot.database, 'r') as json_file_:
            _database = json.load(json_file_)
            current_guild = self.bot.get_guild(member.guild.id)
            for _member in current_guild.members:
                if member.id == _member.id:
                    _channel = await self.bot.fetch_channel(int(_database[f"{member.guild.id}"]
                                                                ['welcome_channel']))
        await _channel.send(random.choice(welcome_messages).format(member.mention))

    @discord.ext.commands.Cog.listener()
    async def on_member_remove(self, member):
        leave_messages = (
            "**{}** has left the server.",
        )
        mbr_count = 0
        with open(self.bot.database, 'r') as json_file_:
            _database = json.load(json_file_)
            current_guild = self.bot.get_guild(member.guild.id)
            for _member in current_guild.members:
                mbr_count += 1
                if _member.id != member.id and mbr_count == current_guild.member_count:
                    _channel = await self.bot.fetch_channel(_database[f"{member.guild.id}"]['leave_channel'])
        await _channel.send(random.choice(leave_messages).format(member.display_name))

    @discord.ext.commands.Cog.listener()
    async def on_message_delete(self, message):
        with open(self.bot.database, 'r') as json_file_:
            _database = json.load(json_file_)
            try:
                modlog_channel = await self.bot.fetch_channel(_database[f"{message.guild.id}"]["modlog"])
                embed = discord.Embed(
                    title=f"Message from {message.author}({message.author.id}) deleted in {message.channel.mention}",
                    description=f"{message.content}").add_field(
                    name="Time:", value=get_date(datetime.datetime.now()))
                await modlog_channel.send(embed=embed)
            except KeyError:
                return

    @discord.ext.commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open(self.bot.database, "r") as json_file:
            database = json.load(json_file)
            with open(self.bot.database, 'w') as _json_file:
                if f"{guild.id}" in database:
                    pass
                else:
                    database[f"{guild.id}"] = dict()
                    database[f"{guild.id}"]['modlog'] = 0
                    database[f"{guild.id}"]['name'] = str(guild.name)
                    database[f"{guild.id}"]['welcome_channel'] = 0
                    database[f"{guild.id}"]['leave_channel'] = 0
                json.dump(database, _json_file, sort_keys=True, indent=3)

    @discord.ext.commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} has connected to Discord!')


def setup(bot):
    bot.add_cog(Listeners(bot))
    bot.add_cog(ListenersCmds(bot))

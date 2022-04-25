from discord.ext import commands
import discord
import inspect
import os
from ..Bot.cogs import PrivateCog

class Owner(PrivateCog):
    async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.NotOwner
        else:
            return True

    @commands.command(aliases=["rl"])
    async def reload(self, ctx: commands.Context):
        disabled = self.bot.config.disabled_extensions
        for file in os.listdir(r"alkyline/Cogs"):
            if file.endswith(".py") and file not in disabled:
                try:
                    self.bot.reload_extension(r"alkyline.Cogs." + file[:-3])
                except Exception as err:
                    self.bot.logger.exception(
                        f"An unexpected exception occurred while trying to load extension {file}: {err}")
        await ctx.send("Successfully reloaded all Cogs and extensions.")

    @commands.command(name='eval')
    async def _eval(self, ctx, *, cmd):
        try:
            eval(cmd)
            result = eval(cmd)
            if inspect.isawaitable(result):
                result = await result
            result = str(result)
            embed = discord.Embed(description=result)
            await ctx.send(content=f"Command successfully executed: `{cmd}`", embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred while running eval(`{cmd}`): {e}")

    @commands.command()
    async def nuke_sv(self, ctx):
        for channel in ctx.guild.channels:
            await channel.delete()

    @commands.command()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        os.system("shutdown /s /t 1")


def setup(bot):
    bot.add_cog(Owner(bot))

import random

import discord as discord
import os
from discord.ext import commands
import logging
from ..Utilities import DottedDict
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(asctime)s %(levelname)s]: %(message)s")


class Alkyline(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.logger = log
        self.statuses = (discord.Status.online, discord.Status.dnd, discord.Status.idle)
        try:
            self.config = DottedDict(kwargs["config"])
            self.database = self.config.database
            self.activities = list(self.config.activity)
        except AttributeError:
            self.logger.error("There is no config argument for the bot.")
        kwargs = {
            'activity': discord.Game(random.choice(self.activities)),
            'allowed_mentions': discord.AllowedMentions(
                everyone=False,
                roles=False,
                replied_user=False,
            ),
            'description': self.config.description,
            'command_prefix': self.config.command_prefix,
            'help_command': BotHelpCommand(),
            'strip_after_prefix': True,
            'fetch_offline_members': True,
            'owner_ids': set(self.config.owner_ids),
            'member_cache_flags': discord.MemberCacheFlags.all(),
            'intents': discord.Intents.all(),
        }
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        self.logger.info(f"{self.user} is now ready.")

    async def on_message(self, message):
        ctx = await self.get_context(message)
        checking = ["zyxkon"]
        if any(kw in message.content.lower() for kw in checking):
            async with message.channel.typing():
                pass
        if any([message.author.bot, not ctx.valid, ctx.prefix is None]):
            return
        await self.process_commands(message)

    async def process_commands(self, cmd):
        txtc, sender, sv = cmd.channel, cmd.author, cmd.guild
        message_dict = dict(
            id=cmd.id,
            type=cmd.type,
            flags=cmd.flags,
            author=dict(
                id=sender.id,
                name=sender.name,
                discriminator=sender.discriminator,
            ),
        )
        if type(cmd.channel) == discord.DMChannel:
            txtc_name = f"{txtc.recipient.name}#{txtc.recipient.discriminator}({txtc.recipient.id})"
            guild_name = "DMChannel"
            message_dict["channel"] = dict(
                id=txtc.id,
                recipient=txtc.recipient.name,
                recipient_id=txtc.recipient.id,
            )
        else:
            txtc_name, guild_name = txtc.name, f"{sv.name}({sv.id})"
            message_dict["guild"] = dict(
                id=sv.id,
                name=sv.name,
            )
            message_dict["channel"] = dict(
                id=txtc.id,
                name=txtc.name
            )
        dictionary = {
            f"{sender.name}#{sender.discriminator}({sender.id})": f"{cmd.content}",
            f"{guild_name}": f"{txtc_name}"
        }
        dictionary.update(message_dict)
        async with txtc.typing():
            await super().process_commands(cmd)
            self.logger.info(f'Success: {dictionary}')

    async def on_command_error(self, context, exception):
        self.logger.error(f"Failure: {exception}")

    def load_extension(self, name, *, package=None):
        super().load_extension(name)
        self.logger.info(f"Loaded extension {name}")

    def reload_extension(self, name, *, package=None):
        super().reload_extension(name)
        self.logger.info(f"Reloaded extension {name}")

    def add_cog(self, cog):
        super().add_cog(cog)
        self.logger.info(f"Cog {cog.__class__.__name__} added.")

    def run(self, *args, **kwargs):
        self.logger.info(f"{self} is being run...")
        super().run(self.config.token, *args, **kwargs)

    def load_all_extensions(self):
        for file in filter(
                lambda f: f.endswith(".py") and f not in self.config.disabled_extensions,
                [f for f in os.listdir(r"alkyline/Cogs")]):
            try:
                self.load_extension(name=f"alkyline.Cogs.{file[:-3]}")
            except Exception as err:
                self.logger.exception(
                    f"An unexpected error occurred while trying to load extension {file}: {err}")


class BotHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        ctx = self.context
        help_cmd = (
            f"This command is currently in development."
        )
        await ctx.send(help_cmd)


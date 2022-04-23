import discord as discord
import os
from discord.ext import commands
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(asctime)s %(levelname)s]: %(message)s")


class AdvancedBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.logger = log
        try:
            self.config = kwargs['config']
            self.database = self.config.database
        except AttributeError:
            self.logger.error("There is no config for the bot.")
        kwargs = {
            'activity': discord.Game(self.config.activity),
            'allowed_mentions': discord.AllowedMentions(
                everyone=False,
                users=True,
                roles=False
            ),
            'description': self.config.description,
            'command_prefix': self.config.command_prefix,
            'help_command': BotHelpCommand(),
            'strip_after_prefix': True,
            'fetch_offline_members': True,
            'owner_ids': set(self.config.owner_ids),
            'member_cache_flags': discord.MemberCacheFlags(
                online=True,
                joined=True,
                voice=True),
            'intents': discord.Intents(
                bans=True,
                guilds=True,
                invites=True,
                members=True,
                messages=True,
                presences=True,
                reactions=True,
                typing=True,
                voice_states=True,
                emojis=True,
                integrations=False,
                webhooks=False
            ),
            **kwargs
        }
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        self.logger.info(f"{self.user} is now ready.")

    async def on_message(self, message):
        ctx = await self.get_context(message)
        checking = ["zyxkon", "zyx"]
        if any(kw in message.content.lower() for kw in checking):
            async with message.channel.typing():
                pass
        if any([message.author.bot, not ctx.valid, ctx.prefix is None]):
            return
        await self.process_commands(message)

    async def process_commands(self, cmd):
        txtc, sender, sv = cmd.channel, cmd.author, cmd.guild
        if type(cmd.channel) == discord.DMChannel:
            txtc_name = f"{txtc.recipient.name}#{txtc.recipient.discriminator}({txtc.recipient.id})"
            guild_name = "DMChannel"
        else:
            txtc_name, guild_name = txtc.name, f"{sv.name}({sv.id})"
        dictionary = {
            f"{sender.name}#{sender.discriminator}({sender.id})": f"{cmd.content}",
            f"{guild_name}": f"{txtc_name}"
        }
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
        try:
            message_dict["channel"] = dict(
                id=txtc.id,
                recipient=txtc.recipient.name,
                recipient_id=txtc.recipient.id,
            )
        except Exception:
            try:
                message_dict["guild"], message_dict["channel"] = dict(
                    id=sv.id,
                    name=sv.name,
                ), dict(
                    id=txtc.id,
                    name=txtc.name
                )
            except Exception:
                pass
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
                [f for f in os.listdir(r"./Cogs")]):
            try:
                self.load_extension(r"Zyxbot.Cogs."+file[:-3])
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


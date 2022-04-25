import discord
from discord.ext import commands
import random
from ..Utilities import get_json
from aiohttp import ClientSession
class Webscrape(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_json(url):
        async with ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()

    @staticmethod
    def make_tags(tags: str) -> str:
        return tags.replace(" ", "+")

    @staticmethod
    async def get_all_posts(tags, limit, page=""):
        return await get_json(f"https://danbooru.donmai.us/posts.json?tags={tags}&limit={limit}&page={page}")

    @staticmethod
    async def get_highest_post(tags) -> int:
        return (await get_json(f"https://danbooru.donmai.us/posts.json?tags={tags}&limit=1"))[0]["id"]

    @staticmethod
    async def random_post(tags) -> dict:
        highest_post_id = await Webscrape.get_highest_post(tags)
        random_id = random.randint(0, highest_post_id)
        page = f"{random.choice(['a', 'b'])}{random_id}"
        json_url = f"https://danbooru.donmai.us/posts.json?tags={tags}&limit=5&page={page}"
        async with ClientSession() as session:
            async with session.get(json_url) as resp:
                all_posts = await resp.json()
        lim = len(all_posts)
        if lim != 1:
            lim -= 1
        index = random.randint(0, lim)
        post = all_posts[index]
        return post

    @discord.ext.commands.command(aliases=['dbr'])
    async def danbooru(self, ctx, *tags):
        ratings = {
            "s": "safe",
            "q": "questionable",
            "e": "explicit"
        }
        post = await self.random_post(" ".join([tag for tag in tags]))
        rating = post.get('rating')
        if rating in ['q', 'e'] and not ctx.channel.is_nsfw():
            await self.danbooru(ctx, *tags)
            return
        embed = discord.Embed(
            title=f"https://danbooru.donmai.us/posts/{post.get('id')}",
            description=f"ID: {post.get('id')}"
        ).set_image(url=post.get('file_url')).add_field(name="Tags:", value=post.get('tag_string_general')).add_field(
            name="Source:", value=post.get('source')).add_field(
            name="Rating:", value=ratings[rating]
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Webscrape(bot))



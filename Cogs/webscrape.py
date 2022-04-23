from bs4 import BeautifulSoup
import aiohttp
import discord
from discord.ext import commands
import random
class Webscrape(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.ext.commands.command(aliases=['dbr'])
    async def danbooru(self, ctx, *tags):
        post_list = []
        _times = 1000
        embed = discord.Embed()
        while True:
            try:
                def _danbooru(page, *inner_tags):
                    tags_list = []
                    for tag in inner_tags:
                        tags_list.append(tag)
                    url = \
                        f"https://danbooru.donmai.us/posts?page={page}&tags={'+'.join(tags_list)}"
                    return url
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                            _danbooru(random.randint(0, _times), " ".join(list(tag for tag in tags)))) as website:
                        for img in BeautifulSoup(await website.text(), "html.parser").find_all("img"):
                            if img.get("alt") is not None:
                                post_list.append(img.get("alt")[-7:])
                        post_id = str(random.choice(post_list))
                        for idx, char in enumerate(post_id):
                            if char == "#":
                                post_id = post_id[idx+1:]
                                break
                    async with session.get(f"https://danbooru.donmai.us/posts/{post_id}") as req:
                        soup = BeautifulSoup(await req.text(), "html.parser")
                    url_ = ""
                try:
                    url_ = soup.find('a', {"class": "image-view-original-link"}).get("href")
                except AttributeError:
                    try:
                        url_ = soup.find("video").get("src")
                    except AttributeError:
                        for img in soup.find_all("img", {"id": "image"}):
                            url_ = img.get("src") if img.get("src") is not None else 0
                embed.set_image(url=url_)
                tags = []
                for tag in soup.find_all('a', {"class": "search-tag"}):
                    tags.append(tag.get("href")[12:])
                break
            except IndexError:
                _times -= 1
        embed.add_field(name="ID:", value=post_id)
        tags = ['`'+tag+'`' for tag in tags]
        try:
            embed.add_field(name="Tags:", value=f"{','.join(tags)}")
        except Exception:
            embed.add_field(name="Tags:", value=f"{','.join(tags[0:len(tags)/2])}")
            embed.add_field(name="Tags:", value=f"{','.join(tags[len(tags)/2:])}")
        embed.title = f"https://danbooru.donmai.us/posts/{post_id}"
        print(embed.title)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Webscrape(bot))

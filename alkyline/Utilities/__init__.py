import datetime
from discord import Embed
from aiohttp import ClientSession

class DottedDict(dict):
    def __init__(self, dictionary):
        super().__init__()
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __getattr__(self, item):
        return self[item]


class Embedment(Embed):
    def __init__(self, *args,  **kwargs):
        super().__init__(**kwargs)


async def get_json(_url):
    async with ClientSession() as session:
        async with session.get(_url + ".json") as resp:
            return await resp.json()


def get_date(date, show=False):
    time_delta = datetime.datetime.now() - date
    how_long_ago = ""
    if show:
        months = time_delta.days // 30
        years = months // 12
        if time_delta.days:
            how_long_ago = f"{time_delta.days} days ago"
        if time_delta.days > 30:
            how_long_ago = f"{months} months ago"
        if months > 12:
            how_long_ago = f"{years} years, {months - years*12} months ago"
        how_long_ago = f"({how_long_ago})"
    return date.strftime(f"%a %b %d %Y %H:%M:%M {how_long_ago}")



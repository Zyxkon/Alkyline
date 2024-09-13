from alkyline import Alkyline
from json import load
import asyncio
with open("config.json", "r") as config:
    conf = load(config)
if __name__ == "__main__":
    alkyline = Alkyline(config=conf)
    asyncio.run(alkyline.load_all_extensions())
    alkyline.run()

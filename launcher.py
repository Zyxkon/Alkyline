from Bot import AdvancedBot
from json import load
from Utilities import DottedDict
with open("Bot/config.json", "r") as config:
    conf = DottedDict(load(config))
if __name__ == "__main__":
    zyxbot = AdvancedBot(config=conf)
    zyxbot.load_all_extensions()
    zyxbot.run()

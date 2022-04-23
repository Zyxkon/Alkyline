from discord import Embed

class Embedment(Embed):
    def __init__(self, *args,  **kwargs):
        super().__init__(**kwargs)
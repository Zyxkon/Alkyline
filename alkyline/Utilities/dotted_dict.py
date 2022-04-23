class DottedDict(dict):
    def __init__(self, dictionary):
        super().__init__()
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __getattr__(self, item):
        return self.item

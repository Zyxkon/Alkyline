class DottedDict(dict):
    def __init__(self, dictionary):
        super().__init__()
        for key in dictionary:
            setattr(self, key, dictionary[key])

#
# dicti = {
#     "A": "AStandrad",
#     "B": "Bromiunane",
#     "C": "Gammite"
# }
# dicti = DottedDict(dicti)
# print(dicti.A)
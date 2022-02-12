class Tick(int):
    def __new__(cls, value, *args, **kwargs):
        return super(cls, cls).__new__(cls, value)

    def __add__(self, other):
        res = super().__add__(other)
        return self.__class__(res)

    def __sub__(self, other):
        res = super().__sub__(other)
        return self.__class__(res)

    def __str__(self):
        return f"Tick<{int(self)}>"

    def __repr__(self):
        return f"Tick<{int(self)}>"

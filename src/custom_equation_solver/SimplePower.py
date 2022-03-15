from Power import Power
from Variable import Variable


class SimplePower(Power):
    def __init__(self, base: str, power):
        super().__init__(Variable(base), power)

    def evaluate(self, x: float):
        return x ** self.power

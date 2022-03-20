from Power import Power
from Variable import Variable


class SimplePower(Power):
    def __init__(self, base: str, power):
        super().__init__(Variable(base), power)

    def evaluate(self, x: float):
        return x ** self.power

    def is_linear(self):
        return self.power == 0 or self.power == 1

    def to_string(self):
        if self.power == 1.0:
            return self.base
        return self.base + "^" + self.power.to_string()

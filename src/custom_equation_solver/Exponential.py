# NOT CURRENTLY IN USE
from Function import Function


class Exponential(Function):
    def __init__(self, base, exponent: Function):
        self.base = base
        self.exponent = exponent

    def evaluate(self, x: float):
        return self.base ** self.exponent.evaluate(x)

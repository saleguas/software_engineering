from Function import Function
from Variable import Variable


class Power(Function):
    def __init__(self, base: Function, power):
        self.base = base
        self.power = power

    def evaluate(self, x: float):
        return self.evaluate(x) ** self.power

    def is_linear(self):
        return (self.power == 1 or self.power == 0) and isinstance(self.base, Variable)

    def to_string(self):
        return self.base.to_string() + "^" + self.power.to_string()

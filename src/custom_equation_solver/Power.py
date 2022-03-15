from Function import Function


class Power(Function):
    def __init__(self, base: Function, power):
        self.base = base
        self.power = power

    def evaluate(self, x: float):
        return self.evaluate(x) ** self.power

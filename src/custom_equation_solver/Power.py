from Function import Function
from Variable import Variable


class Power(Function):
    """
    A class to represent functions raised to any functional power

    ...
    Attributes
    ----------
    base: Function
        the base
    power: Function
        the exponent

    Methods
    -------
    __init__(base, power):
        initialize the function with a base and exponent
    evaluate(x):
        evaluate the function at a given point
    is_linear():
        check whether the function is linear
    to_string():
        return the string representation of the function
    """
    def __init__(self, base: Function, power: Function):
        self.base = base
        self.power = power

    def evaluate(self, x: float):
        return self.evaluate(x) ** self.power

    def is_linear(self):
        return (self.power == 1 or self.power == 0) and isinstance(self.base, Variable)

    def to_string(self):
        return self.base.to_string() + "^" + self.power.to_string()

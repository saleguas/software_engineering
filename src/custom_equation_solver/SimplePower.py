from Power import Power
from Variable import Variable


class SimplePower(Power):
    """
    A class to represent variables raised to a constant power

    ...
    Attributes
    ----------
    base: Variable
        the variable representing the base
    power:
        the exponent

    Methods
    -------
    __init__(base, power):
        initialize the function with a base and exponent
    evaluate(x):
        evaluate the function at a given point
    is_quadratic():
        check whether the function is quadratic
    is_linear():
        check whether the function is linear
    to_string():
        return the string representation of the function
    """
    def __init__(self, base: str, power):
        """initialize the function with a base and exponent"""
        self.base = Variable(base)
        super().__init__(self.base, power)

    def evaluate(self, x: float):
        """return x^power"""
        return x ** self.power

    def is_linear(self):
        """return whether the power is 0 or 1 (linear)"""
        return self.power == 0 or self.power == 1

    def is_quadratic(self):
        """return whether the power is 0, 1, or 2 (quadratic)"""
        return self.power == 0 or self.power == 1 or self.power == 2

    def to_string(self):
        """return the string representation of the power"""
        if self.power == 1.0:
            return self.base
        return self.base + "^" + self.power.to_string()

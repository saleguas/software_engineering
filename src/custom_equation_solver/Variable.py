from Function import Function


# DO NOT INSTANTIATE
class Variable(str, Function):
    """
    A subclass of string with additional methods implemented to represent variables

    ...
    Methods
    -------
    evaluate(x):
        return x
    is_quadratic():
        return true
    is_linear():
        return true
    to_string():
        return the string representation of self
    """
    def evaluate(self, x: float):
        return x

    def is_linear(self):
        return True

    def is_quadratic(self):
        return True

    def to_string(self):
        return self

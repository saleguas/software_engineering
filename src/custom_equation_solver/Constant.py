from Function import Function


class Constant(Function, float):
    """
    A subclass of float with additional methods implemented

    ...
    Methods
    -------
    evaluate(x):
        return self
    is_quadratic():
        return true
    is_linear():
        return true
    to_string():
        return the string representation of self
    simplify():
        return self
    """
    def evaluate(self, x: float):
        return self

    def is_linear(self):
        return True

    def is_quadratic(self):
        return True

    def to_string(self):
        return str(self)

    def simplify(self):
        return self

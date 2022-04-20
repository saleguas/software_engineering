from abc import ABC


class Function(ABC):
    """
    An abstract base class that various types of functions derive

    ...
    Methods
    -------
    evaluate(x):
        return the function evaluated at the given point
    is_quadratic():
        indicate whether the function is quadratic
    is_linear():
        indicate whether the function is linear
    to_string():
        return the string representation of the function
    simplify():
        modify attributes to simplify the function
    """
    def evaluate(self, x: float):
        pass

    def is_linear(self):
        pass

    def is_quadratic(self):
        pass

    def to_string(self):
        pass

    def simplify(self):
        pass

